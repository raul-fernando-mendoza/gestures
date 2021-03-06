//
//  GameScene.swift
//  Sounder
//
//  Created by administrador on 27/12/21.

// Go to your Iphone Settings -> General -> Device Management and "trust" yourself as developer.

import SpriteKit
import GameplayKit
import CoreBluetooth
import AVFoundation

extension String {
    func leftPadding(toLength: Int, withPad character: Character) -> String {
        let newLength = self.count
        if newLength < toLength {
            return String(repeatElement(character, count: toLength - newLength)) + self
        } else {
            return self.substring(from: index(self.startIndex, offsetBy: newLength - toLength))
        }
    }
}



class GameScene: SKScene {
  
    private var label : SKLabelNode?
    private var statusLabel :SKLabelNode =  SKLabelNode(fontNamed: "Arial")
    private var setupLabel :SKLabelNode =  SKLabelNode(fontNamed: "Arial")
    private var spinnyNode : SKShapeNode?
    

    public func setStatusMessage(_ msg:String){
        statusLabel.text = msg
    }
    
    public func setUp(){
        q.startSetup()
    }
    
    
    
    override func sceneDidLoad(){
      
      //  b = BLE("0000ffe0-0000-1000-8000-00805f9b34fb","0000FFE1-0000-1000-8000-00805F9B34FB",self)
        
        //setStatusMessage("discovering BLE...")
        
        setupLabel.name = "setupLabel"
        setupLabel.text = "SETUP"
        setupLabel.fontSize = 12
        setupLabel.fontColor = SKColor.green
        setupLabel.position = CGPoint(x: 10, y: 100) //CGPoint(x: frame.midX, y: frame.midY)
       
        addChild(setupLabel)
        
   
        statusLabel.name = "message"
        statusLabel.text = "You Win!"
        statusLabel.fontSize = 12
        statusLabel.fontColor = SKColor.green
        statusLabel.position = CGPoint(x: 10, y: 20) //CGPoint(x: frame.midX, y: frame.midY)
       
        addChild(statusLabel)
       
    }

    override func didMove(to view: SKView) {
        
        
        /* Create shape node to use during mouse interaction
        let w = (self.size.width + self.size.height) * 0.05
        self.spinnyNode = SKShapeNode.init(rectOf: CGSize.init(width: w, height: w), cornerRadius: w * 0.3)
        
        if let spinnyNode = self.spinnyNode {
            spinnyNode.lineWidth = 2.5
            
            spinnyNode.run(SKAction.repeatForever(SKAction.rotate(byAngle: CGFloat(Double.pi), duration: 1)))
            spinnyNode.run(SKAction.sequence([SKAction.wait(forDuration: 0.5),
                                              SKAction.fadeOut(withDuration: 0.5),
                                              SKAction.removeFromParent()]))
        }
         */
    }
    

    
    func touchDown(atPoint pos : CGPoint) {
        Log.debug("touche down")
        

    }
    
    func touchMoved(toPoint pos : CGPoint) {
        let node = self.childNode(withName: "setupLabel") as? SKLabelNode
        /*
        if let n = self.spinnyNode?.copy() as! SKShapeNode? {
            n.position = pos
            n.strokeColor = SKColor.blue
            self.addChild(n)
        }
         */
    }
    
    func touchUp(atPoint pos : CGPoint) {
        let node = self.childNode(withName: "//setupLabel") as? SKLabelNode
        /*
        if let n = self.spinnyNode?.copy() as! SKShapeNode? {
            n.position = pos
            n.strokeColor = SKColor.red
            self.addChild(n)
        }
         */
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        let buttonSetup = self.childNode(withName: "//setupLabel") as? SKLabelNode
       // let buttonMoveSetup = self.childNode(withName: "//buttonMoveSetup") as? SKLabelNode
        

        
        for t in touches {
            if buttonSetup!.contains(t.location(in: self)){
                Log.debug("click over setup")
            //    q.startSetup()
                setStatusMessage("Setup initiated do not move")
            }
            /*
            if buttonMoveSetup!.contains(t.location(in: self)){
                self.setupMove = true
                self.setupMoveCnt = 0
                self.setStatusMessage(msg: "Please move A LOT")
                for (i, _) in self.limitsMoveUp.enumerated() {
                    self.limitsMoveUp[i] = nil
                    self.limitsMoveDown[i] = nil
                }
                break
            }
             */
         
         }
         
        
    }
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        let node = self.childNode(withName: "//statusLabel") as? SKLabelNode
        //for t in touches { self.touchMoved(toPoint: t.location(in: self)) }
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        //for t in touches { self.touchUp(atPoint: t.location(in: self)) }
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent?) {
        //for t in touches { self.touchUp(atPoint: t.location(in: self)) }
    }
    
    
    override func update(_ currentTime: TimeInterval) {
        // Called before each frame is rendered
    }
}
