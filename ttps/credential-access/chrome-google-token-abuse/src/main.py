# flake8: noqa
#!/usr/bin/env python3
"""
Chrome Token Extractor and Google OAuth Cookie Generator

This script extracts tokens from Chrome's Web Data file, uses them to request
Google OAuth tokens, and formats them into browser-compatible cookies.
"""

import argparse
import logging
import os
import sys

# Import from our modules
from chrome_extractor import ChromeCredentialExtractor, ChromeProfileManager
from token_processor import CookieFormatter, GoogleTokenProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Chrome Token Extractor and Google OAuth Cookie Generator"
    )

    # Output options
    parser.add_argument(
        "--output",
        default="cookies.json",
        help="Output file for cookies (default: cookies.json)",
    )

    # Timeout option
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout for keychain access in seconds (default: 30)",
    )

    # Verbose logging
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()

    # Configure logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # List available Chrome profiles
    available_profiles = ChromeProfileManager.list_available_profiles()
    if not available_profiles:
        logger.error("No Chrome profiles found")
        return 1

    logger.info(
        f"Found {len(available_profiles)} Chrome profiles: {', '.join(available_profiles)}"
    )

    # Dictionary to store successful profile data
    successful_profiles = {}
    storage_password = None

    # Process all profiles
    for profile in available_profiles:
        logger.info(f"Attempting to extract tokens from profile: {profile}")

        try:
            with ChromeCredentialExtractor(
                profile=profile, timeout=args.timeout
            ) as extractor:
                # Create temporary copy of Web Data
                temp_dir = extractor.create_temp_copy()
                if not temp_dir:
                    logger.warning(
                        f"Failed to create temporary copy of Chrome data for profile {profile}"
                    )
                    continue

                # Get Chrome safe storage password (only need to do this once)
                if not storage_password:
                    storage_password = extractor.get_chrome_storage_pass()
                    if not storage_password:
                        logger.error("Failed to retrieve Chrome safe storage password")
                        return 1
                else:
                    # Reuse the storage password for other profiles
                    extractor.storage_password = storage_password

                # Derive master key
                master_key = extractor.derive_master_key()
                if not master_key:
                    logger.warning(f"Failed to derive master key for profile {profile}")
                    continue

                # Extract tokens
                tokens = extractor.extract_tokens()
                if not tokens:
                    logger.warning(f"No tokens found in profile {profile}")
                    continue

                logger.info(f"Extracted {len(tokens)} tokens from profile {profile}")

                # Process Google tokens
                processor = GoogleTokenProcessor()
                google_token = processor.find_google_token(tokens)

                if not google_token:
                    logger.warning(f"No Google token found in profile {profile}")
                    continue

                # Store the successful profile data
                successful_profiles[profile] = {
                    "tokens": tokens,
                    "google_token": google_token,
                }
                logger.info(f"Successfully found Google token in profile: {profile}")

        except Exception as e:
            logger.warning(f"Error processing profile {profile}: {e}")
            continue

    # Check if we found any valid tokens
    if not successful_profiles:
        logger.error("No valid Google tokens found in any Chrome profile")
        return 1

    logger.info(
        f"Found Google tokens in {len(successful_profiles)} profiles: {', '.join(successful_profiles.keys())}"
    )

    # Process each successful profile
    successful_count = 0
    for profile, data in successful_profiles.items():
        try:
            # Generate output filename based on profile
            if args.output == "cookies.json":
                # If using default output name, add profile name
                output_file = f"cookies_{profile.replace(' ', '_').lower()}.json"
            else:
                # If custom output name, add profile name before extension
                base, ext = os.path.splitext(args.output)
                output_file = f"{base}_{profile.replace(' ', '_').lower()}{ext}"

            logger.info(f"Processing profile {profile}, output file: {output_file}")

            # Process the Google token
            processor = GoogleTokenProcessor()

            # Request OAuth tokens
            oauth_response = processor.request_oauth_tokens(data["google_token"])
            if not oauth_response:
                logger.error(f"Failed to request OAuth tokens for profile {profile}")
                continue

            # Validate OAuth response
            if not processor.validate_oauth_response(oauth_response):
                logger.error(f"OAuth response validation failed for profile {profile}")
                continue

            # Get cookies from response
            cookies = processor.get_cookies(oauth_response)
            if not cookies:
                logger.error(
                    f"Failed to extract cookies from OAuth response for profile {profile}"
                )
                continue

            # Format cookies for browser import
            formatter = CookieFormatter()
            formatted_cookies = formatter.format_cookies(cookies)

            if not formatted_cookies:
                logger.error(f"Failed to format cookies for profile {profile}")
                continue

            # Save cookies to file
            if formatter.save_cookies(formatted_cookies, output_file):
                logger.info(
                    f"Successfully saved cookies for profile {profile} to {output_file}"
                )
                successful_count += 1
            else:
                logger.error(
                    f"Failed to save cookies for profile {profile} to {output_file}"
                )

        except Exception as e:
            logger.error(f"Error processing profile {profile}: {e}")
            continue

    if successful_count > 0:
        logger.info(
            f"Successfully processed {successful_count} out of {len(successful_profiles)} profiles with Google tokens"
        )
        return 0
    else:
        logger.error("Failed to process any profiles successfully")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
