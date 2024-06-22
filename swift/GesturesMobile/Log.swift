//
//  Log.swift
//  Sounder
//
//  Created by administrador on 14/01/22.
//

import Foundation

func f(_ v:Int) -> String{
    let valueString:String = String(format: "%d", v)
    guard 5 > valueString.count else { return valueString }
    
    let padding = String(repeating: " ", count: 5 - valueString.count)
    return padding + valueString
}

class Log{
    
    
    enum LogType: Int {
        case debug = 0, info = 1, error = 2
    }
    private static var level:LogType = LogType.debug;
    
    public static func debug(_ str:String){
      
        if( level.rawValue <= LogType.debug.rawValue ){
            print(str)
        }
    }
    public static func error(_ str:String){
      
        if( level.rawValue <= LogType.error.rawValue ){
            print(str)
        }
    }
    public static func setLevel(_ newLevel:LogType){
        level = newLevel
    }
    
   

}
