//
//  Gesture.swift
//  GesturesMobile
//
//  Created by Raul Mendoza on 2/20/22.
//

import Foundation

struct Gesture{
    var axis:Int = -1
    var directionCurrent:EventType = EventType.rest
    var directionPrevious:EventType = EventType.rest

    var valueCurrent:Float = 0.0
    var valuePrevious:Float = 0.0
    var max:Float = 0.0
    var min:Float = 0.0
    var deltaCurrent:Float = 0.0
    var deltaPrevious:Float = 0.0
    var level:Float = 0.0
    var added:Float = 0.0
    var addedPrevious:Float = 0.0
    var message = ""
    
}

