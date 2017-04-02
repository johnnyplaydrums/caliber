//
//  MainViewController.swift
//  caliber
//
//  Created by John Spencer on 3/6/17.
//  Copyright © 2017 Caliber. All rights reserved.
//

import UIKit
import CoreMotion
import CoreLocation

class MainViewController: UIViewController, CLLocationManagerDelegate {
    
    let CMmanager = CMMotionManager()
    
    // Core Motion Labels
    @IBOutlet weak var x_label: UILabel!
    @IBOutlet weak var y_label: UILabel!
    @IBOutlet weak var z_label: UILabel!
    
    
    
    // Core Location Labels
    
    @IBOutlet weak var latitude: UILabel!
    @IBOutlet weak var longitude: UILabel!
//    @IBOutlet weak var horizontalAccuracy: UILabel!
//    @IBOutlet weak var altitude: UILabel!
//    @IBOutlet weak var verticalAccuracy: UILabel!
//    @IBOutlet weak var distance: UILabel!
    
    let CLmanager = CLLocationManager()
    var startLocation: CLLocation!
    
    
    override func viewDidLoad()
    {
        super.viewDidLoad()
        CMmanager.gyroUpdateInterval = 0.05
        CMmanager.startGyroUpdates()
        
        Timer.scheduledTimer(timeInterval: 0.05, target: self, selector: #selector(MainViewController.update), userInfo: nil, repeats: true)
        
    
        CLmanager.desiredAccuracy = kCLLocationAccuracyBest
        CLmanager.delegate = self
        CLmanager.requestWhenInUseAuthorization()
        CLmanager.startUpdatingLocation()
        startLocation = nil
        
        Timer.scheduledTimer(timeInterval: 0.05, target: self, selector: #selector(MainViewController.locationManager(manager: CLmanager, didUpdateLocations: )), userInfo: nil, repeats: true)
        
    }
    
    
    
    func locationManager(_ manager: CLLocationManager,
                         didUpdateLocations locations: [CLLocation])
    {
        let latestLocation: CLLocation = locations[locations.count - 1]
        
        latitude.text = String(format: "%.4f",
                               latestLocation.coordinate.latitude)
        longitude.text = String(format: "%.4f",
                                latestLocation.coordinate.longitude)
        
        if startLocation == nil {
            startLocation = latestLocation
        }
    }
    
    
    func update()
    {
        if let x_data = CMmanager.gyroData?.rotationRate.x {
            x_label.text = String(x_data)
        }
        if let y_data = CMmanager.gyroData?.rotationRate.y {
            y_label.text = String(y_data)
        }
        if let z_data = CMmanager.gyroData?.rotationRate.z {
            z_label.text = String(z_data)
        }
    }
    
    
}
