//
//  ContentView.swift
//  GesturesMobile
//
//  Created by Raul Mendoza on 2/13/22.
//

import SwiftUI
import SpriteKit

struct ContentView: View {

    
    var scene: SKScene{
        let scene =  GameScene()
        scene.size = CGSize(width: 300, height: 400)
        scene.scaleMode = .fill
        return scene
    }
    var body: some View {
        //Text("Hello, world!")
        //    .padding()
        SpriteView(scene:scene)
            .frame(width:300, height:400)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
