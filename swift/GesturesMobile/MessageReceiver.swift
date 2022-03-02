//
//  MessageReceiver.swift
//  GesturesMobile
//
//  Created by Raul Mendoza on 2/20/22.
//

import Foundation

protocol MessageReceiver{
    mutating func message(_ msg:String) -> Void
    func error(_ msg:String) -> Void
    func status(_ msg:String) -> Void
}
