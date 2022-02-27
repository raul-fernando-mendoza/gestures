//
//  queue.swift
//  Sounder
//
//  Created by administrador on 01/01/22.
//

import Foundation
import AVFoundation
import CoreData

let MAX_EVENT_TIME = 400
let MIN_PEAK = 2000

enum EventType: CaseIterable {
    case rest, up, down, upDown, downUp, upSlowing, downSlowing, changeAxis
}


struct Queue{

    
    private var g:Gesture  = Gesture()
    
    let gX = 0
    let gY = 1
    let gZ = 2
    let aX = 3
    let aY = 4
    let aZ = 5
  
    var setupNoiseLevelsUp:[Int?] = [nil,nil,nil,nil,nil,nil]
    var setupNoiseLevelsDown:[Int?] = [nil,nil,nil,nil,nil,nil]
    
    var limitsMoveUp:[Int?] = [nil,nil,nil,nil,nil,nil]
    var limitsMoveDown:[Int?] = [nil,nil,nil,nil,nil,nil]

    
    var buttonToggleStatus = true
    var buttonCurrentStatus = 1
    var buttonLastDownTime = 0
    var buttonLastUpTime = 0
    var setupRest = true
    var setupCnt = 0
    var setupMove = false
    var setupMoveCnt = 0
    
    let factor:Float = 0.4
    
    let xUpURL = Bundle.main.url(forResource: "python_sounds_4b", withExtension: "wav")
    var playerxUp:[AVAudioPlayer?] = []
    let xDownURL = Bundle.main.url(forResource: "python_sounds_4c", withExtension: "wav")
    var playerxDown:[AVAudioPlayer?] = []
    let yUpURL = Bundle.main.url(forResource: "python_sounds_dum" , withExtension: "wav")
    var playeryUp:[AVAudioPlayer?] = []
    let yDownURL = Bundle.main.url(forResource: "python_sounds_tac" , withExtension: "wav")
    var playeryDown:[AVAudioPlayer?] = []
    
    var playersUp:[[AVAudioPlayer?]] = []
    var playersDown:[[AVAudioPlayer?]] = []
    
    var timePreviousRead:Int = 0

    var log_values:[[Int]] = [ [], [], [] ]
    var fitting_x_values:[Int] = []
    var fitting_y_values:[Int] = []
    let MAX_READS = 5
    let GIROX = 0
    let GIROY = 1
    let GIROZ = 2
    var axis_current = 0
    var fitting_min = 0
    var fitting_max = 0
    var fitting_current_slop = 0
    var canPlayDown = true
    var canPlayUp = true
    let MIN_DIFF = 300
    var fitting_previous_slop = 0
    var rebound_time:Int = 0
    var rebound_value:Int = 0
    
   
    private var initialized = false
    
    init(){
        do{
            try AVAudioSession.sharedInstance().setCategory(
                AVAudioSession.Category.playback,
                options: AVAudioSession.CategoryOptions.mixWithOthers
            )
            try AVAudioSession.sharedInstance().setActive(true)
            
            try playerxUp.append( AVAudioPlayer(contentsOf: xUpURL!) )
            try playerxUp.append( AVAudioPlayer(contentsOf: xUpURL!) )
            
            playersUp.append(playerxUp)
            
            try playerxDown.append( AVAudioPlayer(contentsOf: xDownURL!) )
            try playerxDown.append( AVAudioPlayer(contentsOf: xDownURL!) )
            playersDown.append(playerxDown)
            
            try playeryUp.append( AVAudioPlayer(contentsOf: yUpURL!) )
            try playeryUp.append( AVAudioPlayer(contentsOf: yUpURL!) )
            
            playersUp.append(playeryUp)
            
            try playeryDown.append( AVAudioPlayer(contentsOf: yDownURL!) )
            try playeryDown.append( AVAudioPlayer(contentsOf: yDownURL!) )
            playersDown.append(playeryDown)
            
        } catch{
            Log.error("init")
        }

    }

    
    //find a value removing the rest values
    func removeRestValues(_ value:Int,_ upperLimit:Int,_ lowerLimit:Int) -> Int{
        if( value > upperLimit){
            return value - upperLimit
        }
        else{
            return value - lowerLimit
        }
    }
    func toRange(_ value:Float,_ upperLimit:Float,_ lowerLimit:Float) -> Float{
        return (value - lowerLimit) / (upperLimit - lowerLimit)
    }
    func biggerIndexAgg(_ values:[Float]) -> Int{
        var idx:Int = 0
        for i in 0...2{
            if  abs(values[i]) > abs(values[idx]){
                idx = i
            }
        }
        return idx
    }
    
    mutating func startSetup(){
        setupRest = true
        setupCnt = 0
        for i in 0...5 {
            setupNoiseLevelsUp[i] = nil
            setupNoiseLevelsDown[i] = nil
        }
    }
    func printLimits(){
        var strUp = ""
        var strDown = ""
        for i in 0...5 {
            strUp +=  String(format: "%d", self.setupNoiseLevelsUp[i]!).leftPadding(toLength: 10, withPad: " ") + " "
            strDown += String(format: "%d", self.setupNoiseLevelsDown[i]!).leftPadding(toLength: 10, withPad: " ") + " "
        }
        Log.debug("limits")
        Log.debug(strUp)
        Log.debug(strDown)
    }

    mutating func processMessage(currentTime:Int,raw:[Int],buttonStatus:Int) -> Gesture {
        var gesture = Gesture()
        var values:[Int] = [0,0,0,0,0,0]
        //let ge = GiroEvent( startTime: timePreviousRead,endTime: currentTime,raw: raw, buttonStatus: buttonStatus)
        
        Log.debug("\(currentTime) \(raw) \(buttonStatus)")
        
       
        for j in 0 ... 5 {
            if( setupNoiseLevelsUp[j] != nil && raw[j] >= setupNoiseLevelsUp[j]! ){
                values[j]  = raw[j] - setupNoiseLevelsUp[j]!
            }
            else if( setupNoiseLevelsDown[j] != nil && raw[j] <= setupNoiseLevelsDown[j]! ){
                values[j]  = raw[j] - setupNoiseLevelsDown[j]!
                
            }
            else if( setupNoiseLevelsDown[j] != nil && setupNoiseLevelsUp[j] != nil && setupNoiseLevelsDown[j]! <= raw[j] && raw[j] <= setupNoiseLevelsUp[j]! ){
                values[j]  = 0
            }
            else{
                values[j]  = raw[j]
            }
        }
        
        if log_values[0].count >= MAX_READS{
            log_values[0].remove(at: 0)
            log_values[1].remove(at: 0)
            log_values[2].remove(at: 0)
            fitting_x_values.remove(at: 0)
            
        }

        log_values[0].append(values[GIROX])
        log_values[1].append(values[GIROY])
        log_values[2].append(values[GIROZ])
        fitting_x_values.append(currentTime)
        

        //find out the new active axis
        var axis_new = 0
        var sum0 = 0
        var sum1 = 0
   
        for k in 0 ..< log_values[0].count {
            sum0 += abs(log_values[0][k])
            sum1 += abs(log_values[1][k])
        }
        if sum0 >= sum1 {
            axis_new = 0
        }
        else{
            axis_new = 1
        }
        if axis_current != axis_new{
            axis_current = axis_new
            fitting_min = values[axis_current]
            fitting_max = values[axis_current]
            fitting_current_slop = 0
            canPlayDown = true
            canPlayUp = true
            fitting_y_values = log_values[axis_current]
        }
        
        //canPlay prevent the playing of more than 1 time even if the movement occilate before crossing
        if values[axis_current] > -MIN_DIFF {
          canPlayDown = true
        }
        if values[axis_current] < MIN_DIFF{
          canPlayUp = true
        }


        var currentValue = 0.0
        var nextValue = 0.0
        var (m,c) = (0.0,0.0)

        //creating fitting curve
        if fitting_x_values.count >= MAX_READS{
              var fitting_times_converted:[Double] = [Double](repeating:0.0, count: MAX_READS)
              var fitting_values_converted:[Double] = [Double](repeating:0.0, count: MAX_READS)
              let startTime = fitting_x_values[0]
              for j in 0 ..< fitting_times_converted.count{
                        fitting_times_converted[j] = Double(fitting_x_values[j] - startTime)
                        fitting_values_converted[j] = Double(log_values[axis_current][j])
              }
              //let max_time = fitting_times_converted.max()
              //let min_value = fitting_values_converted.min()
              //let max_value = fitting_values_converted.max()
              let lastTime:Double = fitting_times_converted[ fitting_times_converted.count - 1]
              (m,c) = findBestFit( fitting_times_converted, fitting_values_converted)
              currentValue = CalculateNextValue( lastTime, m, c)
              nextValue = CalculateNextValue( lastTime + 30, m, c)
              
              //calculate the slop
              if Int(nextValue) > Int(currentValue){
                  fitting_current_slop = 1
              }
              else if Int(nextValue) < Int(currentValue){
                  fitting_current_slop = -1
              }
              else{
                  fitting_current_slop = 0
              }

          //calculate fitting min and max will be used to know the amplitud of the movement
              if fitting_current_slop == fitting_previous_slop{
                  if values[axis_current] < fitting_min{
                    fitting_min = values[axis_current]
                  }
                  if values[axis_current] > fitting_max{
                    fitting_max = values[axis_current]
                  }
              }
        }
        if currentTime > rebound_time{
            rebound_value = 0
            rebound_time = 0
        }
        //Log.debug("\(currentTime) \(f(values[0])) \(f(values[1])) \(f(values[2])) \(f(values[3])) \(f(values[4])) \(f(values[5])) b:\(buttonStatus)  s:\(fitting_current_slop) fM:\(f(fitting_max)) fm:\(f(fitting_min)) r:\(f(rebound_value)) t:\(f(rebound_time)) a:\(axis_current) d:\(canPlayDown) u:\(canPlayUp) s0:\(f(sum0)) s1:\(f(sum1)) m:\(m) c:\(c) cv:\(currentValue) nv:\(nextValue)")


        
        if currentTime > rebound_time{
            if  canPlayDown == true && fitting_previous_slop == -1 && fitting_current_slop == 1 && fitting_min < -MIN_PEAK && currentTime > rebound_time{
                
                Log.debug("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< \(fitting_max) - \(fitting_min) >")
                
                let gesture:Gesture = Gesture( axis: axis_current, directionCurrent: EventType.downUp)
                
                play(gesture.axis, gesture.directionCurrent, 1.0)
                canPlayDown = false
                //set rebound
                rebound_time = currentTime + MAX_EVENT_TIME
                
            }
            if canPlayUp == true && fitting_previous_slop == 1 && fitting_current_slop == -1 && fitting_max > MIN_PEAK && currentTime > rebound_time {
                Log.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \(fitting_max) - \(fitting_min)")
                let gesture:Gesture = Gesture(axis: axis_current, directionCurrent: EventType.upDown)
                play(gesture.axis, gesture.directionCurrent, 1.0)
                canPlayUp = false

                //set rebound
                rebound_time = currentTime + MAX_EVENT_TIME
                
            }
        }
        
        if buttonCurrentStatus==1 && buttonStatus == 0 {
            buttonCurrentStatus = 0
            buttonLastDownTime = currentTime
        }
        if buttonCurrentStatus==0 && buttonStatus == 1{
            buttonCurrentStatus = 1
            buttonLastUpTime = currentTime

            buttonToggleStatus  = !buttonToggleStatus
            if buttonToggleStatus {
                Log.setLevel(Log.LogType.debug)
                Log.debug("Restaring DEBUG -----------------------")
                printLimits()
            }
            else{
                Log.setLevel(Log.LogType.error)
            }
        }
        
        if setupRest == true{
            for i in 0...5 {
                if setupNoiseLevelsUp[i] == nil || raw[i] > setupNoiseLevelsUp[i]! {
                    setupNoiseLevelsUp[i] = raw[i]
                }
                if setupNoiseLevelsDown[i] == nil || raw[i] < setupNoiseLevelsDown[i]!{
                    setupNoiseLevelsDown[i] = raw[i]
                }
            }
            setupCnt += 1;
            gesture.message = "stand still \(setupCnt)"
            if setupCnt > 100 {
                setupRest = false
                setupCnt=0
                
                Log.debug("-------------------" + gesture.message + "-----------------")

                printLimits()
            }
        }
        /*
        if setupMove == true{
            for i in 0 ... 5 {
                if limitsMoveUp[i] == nil || raw[i] > limitsMoveUp[i]! {
                    limitsMoveUp[i] = raw[i]
                }
                if limitsMoveDown[i] == nil || raw[i] < limitsMoveDown[i]!{
                    limitsMoveDown[i] = raw[i]
                }
            }
            setupMoveCnt += 1;
            gesture.message =  "keep moving \(setupMoveCnt)"
            if setupMoveCnt > 200 {
                self.setupMove = false
                setupMoveCnt = 0
                gesture.message = "you can STOP moving"
                var strUp = ""
                var strDown = ""
                for i in [Int](0...5) {
                    strUp +=  String(format: "%d", self.limitsMoveUp[i]!).leftPadding(toLength: 10, withPad: " ") + " "
                    strDown += String(format: "%d", self.limitsMoveDown[i]!).leftPadding(toLength: 10, withPad: " ") + " "
                }
                Log.debug("limits Moving")
                Log.debug(strUp)
                Log.debug(strDown)
               
            }
        }
         */
       
        timePreviousRead = currentTime
        
        if fitting_current_slop != fitting_previous_slop{
            fitting_min = values[axis_current]
            fitting_max = values[axis_current]
        }
        fitting_previous_slop = fitting_current_slop
            
        return gesture
    }
     
    func play(_ idx:Int,_ te:EventType,_ volume:Float){
        
        if te == EventType.upDown || te == EventType.upSlowing {
            let playerUp = playersUp[idx]
            if( playerUp[0]!.isPlaying == false){
                
                playerUp[0]!.volume = 1
                playerUp[0]!.play()
            }
            else if( playerUp[1]!.isPlaying == false){
                
                playerUp[1]!.volume = 1
                playerUp[1]!.play()
            }
            else{
                Log.error("ªªªª ERROR UP is already playing")
            }
        }
        else if te == EventType.downUp || te == EventType.downSlowing{
            let playerDown = playersDown[idx]
            if( playerDown[0]!.isPlaying == false){
                
                playerDown[0]!.volume = 1
                playerDown[0]!.play()
            }
            else if( playerDown[1]!.isPlaying == false){
                
                playerDown[1]!.volume = 1
                playerDown[1]!.play()
            }
            else{
                Log.error("ªªªª ERROR UP is already playing")
            }
        }
    }


}
