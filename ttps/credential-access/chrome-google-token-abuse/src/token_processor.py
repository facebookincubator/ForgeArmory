# flake8: noqa
#!/usr/bin/env python3
"""
Google Token Processor

This module provides classes for processing Google tokens and formatting cookies.
"""

import json
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class GoogleTokenProcessor:
    """Processes Google tokens and makes OAuth requests."""

    OAUTH_URL = "https://accounts.google.com/oauth/multilogin"

    def __init__(self):
        """Initialize the Google token processor."""
        self.tokens = None
        self.oauth_response = None

    def find_google_token(self, tokens):
        """
        Finds a Google token in the list of tokens.

        Args:
            tokens: List of token dictionaries

        Returns:
            Dictionary with service and token or None if not found
        """
        if not tokens:
            logger.error("No tokens provided")
            return None

        # Look for Google service tokens
        for token_data in tokens:
            service = token_data.get("service", "")
            # Check for both possible formats of Google tokens
            if service.startswith("AccountId-"):
                logger.info(f"Found Google token for service: {service}")
                return token_data

            # Debug: Print all token services to help identify patterns
            logger.debug(f"Token service found: {service}")

        logger.warning("No Google token found in the provided tokens")
        return None

    def extract_account_id(self, service):
        """
        Extracts the account ID from a Google service string.

        Args:
            service: Google service string

        Returns:
            Account ID or None if not found
        """
        try:
            # Extract numeric account ID from service string
            import re

            match = re.search(r"(\d+)", service)
            if match:
                account_id = match.group(1)
                logger.debug(f"Extracted account ID: {account_id}")
                return account_id
            else:
                logger.warning(f"Could not extract account ID from service: {service}")
                return None
        except Exception as e:
            logger.error(f"Error extracting account ID: {e}")
            return None

    def request_oauth_tokens(self, token_data):
        """
        Makes a request to Google OAuth endpoint using the token.

        Args:
            token_data: Dictionary with service and token

        Returns:
            OAuth response as dictionary or None if failed
        """
        if not token_data:
            logger.error("No token data provided")
            return None

        service = token_data.get("service")
        token = token_data.get("token")

        if not service or not token:
            logger.error("Invalid token data: missing service or token")
            return None

        account_id = self.extract_account_id(service)
        if not account_id:
            return None

        # Form the Authorization header
        auth_header = f"MultiBearer {token}:{account_id}"

        # Use subprocess to execute curl command
        import subprocess

        try:
            # Prepare curl command
            curl_cmd = [
                "curl",
                "-s",
                "-X",
                "POST",
                self.OAUTH_URL,
                "-H",
                f"Authorization: {auth_header}",
                "-H",
                "Accept: */*",
                "-H",
                "User-Agent: com.google.Drive/6.0.230903 iSL/3.4 iPhone/15.7.4 hw/iPhone9_4 (gzip)",
                "-H",
                "Accept-Language: en-US,en;q=0.9",
                "-H",
                "Content-Type: application/x-www-form-urlencoded",
                "-d",
                "source=com.google.Drive",
            ]

            # Execute curl command
            logger.debug("Using curl for HTTP request")
            process = subprocess.Popen(
                curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            stdout, stderr = process.communicate()

            if stderr:
                logger.warning(f"Curl stderr: {stderr}")

            if not stdout:
                logger.error("Empty response from OAuth endpoint")
                return None

            # Parse JSON response
            try:
                # Handle potential non-JSON prefix in response
                if not stdout.startswith("{"):
                    # Find the first JSON opening brace
                    json_start = stdout.find("{")
                    if json_start >= 0:
                        stdout = stdout[json_start:]
                    else:
                        logger.error("Could not find JSON content in response")
                        return None

                response_data = json.loads(stdout)
                self.oauth_response = response_data
                logger.info("Successfully received OAuth response")
                return response_data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.debug(f"Response content: {stdout[:100]}...")
                return None

        except Exception as e:
            logger.error(f"Error making OAuth request: {e}")
            return None

    def validate_oauth_response(self, response=None):
        """
        Validates the OAuth response.

        Args:
            response: OAuth response dictionary

        Returns:
            True if valid, False otherwise
        """
        if response is None:
            response = self.oauth_response

        if not response:
            logger.error("No OAuth response to validate")
            return False

        # Check if the response has a status field
        status = response.get("status")
        if not status:
            logger.error("OAuth response missing status field")
            return False

        # Check if status is OK
        if status.lower() != "ok":
            logger.error(f"OAuth response status not OK: {status}")
            return False

        # Check if cookies are present
        cookies = response.get("cookies")
        if not cookies:
            logger.error("OAuth response missing cookies")
            return False

        logger.info("OAuth response validation successful")
        return True

    def get_cookies(self, response=None):
        """
        Extracts cookies from the OAuth response.

        Args:
            response: OAuth response dictionary

        Returns:
            List of cookie dictionaries or None if failed
        """
        if response is None:
            response = self.oauth_response

        if not response:
            logger.error("No OAuth response to extract cookies from")
            return None

        cookies = response.get("cookies")
        if not cookies:
            logger.error("No cookies found in OAuth response")
            return None

        logger.info(f"Extracted {len(cookies)} cookies from OAuth response")
        return cookies


class CookieFormatter:
    """Formats cookies for browser import."""

    def __init__(self):
        """Initialize the cookie formatter."""
        pass

    def format_cookies(self, cookies):
        """
        Formats cookies according to browser import format.

        Args:
            cookies: List of cookie dictionaries from OAuth response

        Returns:
            List of formatted cookie dictionaries
        """
        if not cookies:
            logger.error("No cookies to format")
            return []

        formatted_cookies = []
        current_time = int(time.time())

        for cookie in cookies:
            # Create a new cookie dictionary with the required format
            formatted_cookie = {}

            # Map fields from OAuth response to browser format
            if "host" in cookie:
                formatted_cookie["domain"] = cookie["host"]
            elif "domain" in cookie:
                formatted_cookie["domain"] = cookie["domain"]
            else:
                logger.warning("Cookie missing domain/host field, skipping")
                continue

            # Copy standard fields
            for field in ["name", "path", "value"]:
                if field in cookie:
                    formatted_cookie[field] = cookie[field]
                else:
                    logger.warning(f"Cookie missing {field} field, using default")
                    formatted_cookie[field] = "" if field != "path" else "/"

            # Set session flag
            formatted_cookie["session"] = False

            # Set hostOnly flag based on cookie name
            special_cookies = [
                "ACCOUNT_CHOOSER",
                "__Host-GAPS",
                "__Host-1PLSID",
                "__Host-3PLSID",
            ]
            formatted_cookie["hostOnly"] = cookie["name"] in special_cookies

            # Convert security flags
            formatted_cookie["secure"] = cookie.get("isSecure", False)
            formatted_cookie["httpOnly"] = cookie.get("isHttpOnly", False)

            # Set expiration date: if greater than 7 days keep in place, if less than, set to 7 days
            seven_days = 7 * 24 * 60 * 60
            if "maxAge" in cookie:
                expiration = current_time + int(cookie["maxAge"])
                if expiration < current_time + seven_days:
                    # If less than 7 days, set to 7 days
                    formatted_cookie["expirationDate"] = current_time + seven_days
                else:
                    # If greater than 7 days, keep the original expiration
                    formatted_cookie["expirationDate"] = expiration
            else:
                # Default to 7 days if no maxAge
                formatted_cookie["expirationDate"] = current_time + seven_days

            # Set sameSite policy only if it exists in the original cookie
            if "sameSite" in cookie or any(
                key.lower() == "samesite" for key in cookie.keys()
            ):
                formatted_cookie["sameSite"] = "no_restriction"

            formatted_cookies.append(formatted_cookie)

        logger.info(f"Formatted {len(formatted_cookies)} cookies for browser import")
        return formatted_cookies

    def save_cookies(self, cookies, file_path):
        """
        Saves formatted cookies to a JSON file.

        Args:
            cookies: List of formatted cookie dictionaries
            file_path: Path to save the cookies file

        Returns:
            True if successful, False otherwise
        """
        if not cookies:
            logger.error("No cookies to save")
            return False

        try:
            with open(file_path, "w") as f:
                json.dump(cookies, f, indent=2)

            logger.info(f"Saved {len(cookies)} cookies to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save cookies to {file_path}: {e}")
            return False
