//
//  BLE.swift
//  GesturesMobile
//
//  Created by Raul Mendoza on 2/20/22.
//

import Foundation
import CoreBluetooth


class BLE: NSObject, CBPeripheralDelegate, CBCentralManagerDelegate{
    
    private var statusMsg:String = "Starting..."
    public var serviceUUID:CBUUID   //  = CBUUID.init(string: "0000ffe0-0000-1000-8000-00805f9b34fb")
    public var characteristicUUID:CBUUID // = CBUUID.init(string: "0000FFE1-0000-1000-8000-00805F9B34FB")

    var receiver:MessageReceiver
    
    
    private var centralManager: CBCentralManager!
    private var peripheral: CBPeripheral!
    
    private var message:String = ""
    

    

    
    init(_ service:String,_ characteristic:String,_ r:MessageReceiver){
        serviceUUID = CBUUID.init(string: service)
        characteristicUUID = CBUUID.init(string: characteristic)
        receiver = r
        super.init()
        print("discovering BLE...")
        centralManager = CBCentralManager(delegate: self, queue: nil)
    }
    

    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        print("Central state update")
        if central.state != .poweredOn {
            receiver.status("Central is not powered on")
        } else {
            receiver.status("Central scanning for");
            centralManager.scanForPeripherals(withServices: [self.serviceUUID],
                                              options: [CBCentralManagerScanOptionAllowDuplicatesKey : true])
        }
    }
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {

        // We've found it so stop scan
        receiver.status("peripheral found");
        self.centralManager.stopScan()

        // Copy the peripheral instance
        self.peripheral = peripheral
        self.peripheral.delegate = self

        // Connect!
        self.centralManager.connect(self.peripheral, options: nil)

    }
    
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        if peripheral == self.peripheral {
            receiver.status("Connecting to service")
            peripheral.discoverServices([serviceUUID])
        }
    }
    
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        if let services = peripheral.services {
            for service in services {
                if service.uuid == self.serviceUUID {
                    receiver.status("service found")
                    //Now kick off discovery of characteristics
                    peripheral.discoverCharacteristics([characteristicUUID], for: service)
                    return
                }
            }
        }
    }
    
    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        if let characteristics = service.characteristics {
            for characteristic in characteristics {
                if characteristic.uuid == characteristicUUID{
                    receiver.status("characteristic found")
                    peripheral.setNotifyValue( true, for: characteristic)
                }
            }
        }
    }
    func peripheral(_ peripheral: CBPeripheral,
           didUpdateValueFor characteristic: CBCharacteristic,
                    error: Error?){
        guard var data:Data = characteristic.value else { return }
        
        let received:String = String(data: data, encoding: .utf8)!
        //print(received)
        
        //print("byte by byte")
        while let b = data.popFirst() {
            //print("\(b) [\(Character(UnicodeScalar(b)))]")
            if b != 13 && b != 10 {
                message = message + String( Character(UnicodeScalar(b)) )
            }
            if b == 13 {
                //do nothing
                var x = b
            }
            else if b==10 {                
                receiver.message(message)
                message = ""
            }
        }
    }
    

}
