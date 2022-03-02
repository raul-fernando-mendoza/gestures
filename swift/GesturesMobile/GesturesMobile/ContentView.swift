//
//  ContentView.swift
//  GesturesMobile
//
//  Created by Raul Mendoza on 2/13/22.
//

import SwiftUI
import SpriteKit

struct Handler: MessageReceiver{
    
   mutating func message(_ msg: String) {
       print(msg)
   }
   
   func error(_ msg: String) {
       
   }
   
   func status(_ msg: String) {
       
   }
}
var handler = Handler()


struct ContentView: View {

    let gameScene =  GameScene()
    
    
    var scene: SKScene{
        
        gameScene.size = CGSize(width: 300, height: 300)
       
        //scene.scaleMode = .fill
        return gameScene
    }
    var body: some View {
        VStack {
            Button("Setup", action: setUp)
            SpriteView(scene:scene)
                .frame(width:300, height:300)
                .border(Color.blue)
                
        }
    }
    func setUp(){
        Log.debug("starting setup")
        gameScene.setUp()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
