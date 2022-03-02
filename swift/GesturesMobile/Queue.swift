//
//  queue.swift
//  Sounder
//
//  Created by administrador on 01/01/22.
//

import Foundation
import AVFoundation
import CoreData

let REBOUND_TIME = 50
let MIN_PEAK = 6000
let MIN_DIFF = 300
	

let xUpURL = Bundle.main.url(forResource: "python_sounds_4c", withExtension: "wav")
var playerxUp:[AVAudioPlayer?] = []
let xDownURL = Bundle.main.url(forResource: "python_sounds_4c", withExtension: "wav")
var playerxDown:[AVAudioPlayer?] = []
let yUpURL = Bundle.main.url(forResource: "python_sounds_dum" , withExtension: "wav")
var playeryUp:[AVAudioPlayer?] = []
let yDownURL = Bundle.main.url(forResource: "python_sounds_tac" , withExtension: "wav")
var playeryDown:[AVAudioPlayer?] = []

var playersUp:[[AVAudioPlayer?]] = []
var playersDown:[[AVAudioPlayer?]] = []


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
    

    
    var timePreviousRead:Int = 0

    var log_values:[[Int]] = [ [], [], [] ]
 
    let MAX_READS = 5
    let GIROX = 0
    let GIROY = 1
    let GIROZ = 2
    var axis_current = 0

    var canPlayDown = true
    var canPlayUp = true

    var fitting_previous_slop = 0
    
  
    
   
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
        
        Log.debug("\(currentTime) \(values) \(buttonStatus)")
        
        if log_values[0].count >= MAX_READS{
            log_values[0].remove(at: 0)
            log_values[1].remove(at: 0)
            log_values[2].remove(at: 0)
        
            
        }

        log_values[0].append(values[GIROX])
        log_values[1].append(values[GIROY])
        log_values[2].append(values[GIROZ])
        
        

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

            canPlayDown = true
            canPlayUp = true
          
        }
        
        //canPlay prevent the playing of more than 1 time even if the movement occilate before crossing
        if values[axis_current] > -MIN_DIFF {
          canPlayDown = true
        }
        if values[axis_current] < MIN_DIFF{
          canPlayUp = true
        }

     

        
        Log.debug("\(currentTime) \(f(values[0])) \(f(values[1])) \(f(values[2])) \(f(values[3])) \(f(values[4])) \(f(values[5])) b:\(buttonStatus)   a:\(axis_current) d:\(canPlayDown) u:\(canPlayUp) s0:\(f(sum0)) s1:\(f(sum1)) ")
         

        
        if  buttonToggleStatus{
            if canPlayDown == true && values[axis_current] < -MIN_PEAK
            {
                Log.debug("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  >")
                
                let gesture:Gesture = Gesture( axis: axis_current, directionCurrent: EventType.downUp)
                
                play(gesture.axis, gesture.directionCurrent, 1.0)
                canPlayDown = false
                

                
            }
            if canPlayUp == true && values[axis_current] > MIN_PEAK  {
                Log.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
                let gesture:Gesture = Gesture(axis: axis_current, directionCurrent: EventType.upDown)
                play(gesture.axis, gesture.directionCurrent, 1.0)
                canPlayUp = false

                

                
            }
        }
        //prevent buttoncurrentstatus from changing many times if button remains down
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
                gesture.message = "You can move now"
                
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
