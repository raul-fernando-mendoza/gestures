//
//  ContentView.swift
//  GesturesMobile
//
//  Created by Raul Mendoza on 2/13/22.
//

import SwiftUI
import SpriteKit

var q:Queue!
var b:BLE?


struct ContentView: View , MessageReceiver{

    

    let gameScene =  GameScene()
    @State private var statusText = "no status"
    
 
    mutating func message(_ msg: String) {
        let split = msg.components(separatedBy: "\t")
        //var timeCurrent:Int? = nil
        if split.count == 8 , let timeCurrent = Int(split[0]),
                      let giroX = Int(split[1]),
                      let giroY = Int(split[2]),
                      let giroZ = Int(split[3]),
                      let accX = Int(split[4]),
                      let accY = Int(split[5]),
                      let accZ = Int(split[6]),
                      let buttonStatus = Int(split[7]) {
                
            let raw:[Int] = [ giroX, giroY, giroZ, accX, accY, accZ ]
            Log.debug("\(timeCurrent) \(raw) \(buttonStatus)")
                
            let g = q.processMessage(currentTime: timeCurrent, raw: raw,buttonStatus: buttonStatus)
            //setStatusMessage(g.message)
        }
        else{
            if split.count > 0 {
                Log.debug("E:\(msg)")
                //setStatusMessage(msg)
            }
        }

    }
    
    func error(_ msg: String) {
        
    }
    
    func status(_ msg: String) {
        statusText = msg
    }
    
    var scene: SKScene{
        
        gameScene.size = CGSize(width: 300, height: 300)
       
        //scene.scaleMode = .fill
        return gameScene
    }
    var body: some View {
        VStack {
            Button(action: setUp) {
                Text("connect")
            }.padding()
            Button(action: setInitialize) {
                Text("setup rest")
            }
            Label {
                Text("\(statusText)")
                    .foregroundColor(.primary)
                    .font(.largeTitle)
                    .padding()
                    .background(.gray.opacity(0.2))
                    .clipShape(Capsule())
            } icon: {
                RoundedRectangle(cornerRadius: 10)
                    .fill(.blue)
                    .frame(width: 64, height: 64)
            }
            SpriteView(scene:scene)
                .frame(width:300, height:300)
                .border(Color.blue)
            
        }
    }
    func setUp(){
        print("hello")
        q = Queue(self)
        b = BLE("0000ffe0-0000-1000-8000-00805f9b34fb","0000FFE1-0000-1000-8000-00805F9B34FB",self)
    }
    func setInitialize(){
        q.startSetup()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
