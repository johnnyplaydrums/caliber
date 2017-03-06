//
//  MainViewController.swift
//  caliber
//
//  Created by John Spencer on 3/6/17.
//  Copyright © 2017 Caliber. All rights reserved.
//

import UIKit
import CoreMotion

class MainViewController: UIViewController {
    
    let manager = CMMotionManager()

    @IBOutlet weak var x_label: UILabel!
    @IBOutlet weak var y_label: UILabel!
    @IBOutlet weak var z_label: UILabel!
    override func viewDidLoad() {
        manager.gyroUpdateInterval = 0.05
        manager.startGyroUpdates()
        Timer.scheduledTimer(timeInterval: 0.05, target: self, selector: #selector(MainViewController.update), userInfo: nil, repeats: true)
        super.viewDidLoad()
    }
    
    func update() {
        if let x_data = manager.gyroData?.rotationRate.x {
            x_label.text = String(x_data)
        }
        if let y_data = manager.gyroData?.rotationRate.y {
            y_label.text = String(y_data)
        }
        if let z_data = manager.gyroData?.rotationRate.z {
            z_label.text = String(z_data)
        }
    }
    
}
