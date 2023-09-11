import Foundation

typealias addFunc = @convention(c) (CInt,CInt) -> CInt

do {
let dispatch = DispatchQueue.global(qos: .background)
        let myhandle = dlopen("calc.dylib", RTLD_GLOBAL)
        if (myhandle != nil){
                dispatch.async{
                    DispatchQueue.main.async {
                        let x = dlsym(myhandle, "_main") //for calling main in C built dylibs, use _main
                if (x != nil){
                       print(x)
               }
                dlclose(myhandle)
                    }


                }

        }
} catch let(err){
        print(err)
}

RunLoop.main.run()
