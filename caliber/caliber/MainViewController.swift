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
    let CLmanager = CLLocationManager()
    var startLocation: CLLocation!
    
    // Core Motion Labels
    @IBOutlet weak var x_label: UILabel!
    @IBOutlet weak var y_label: UILabel!
    @IBOutlet weak var z_label: UILabel!
    
    // Core Location Labels
    @IBOutlet weak var latitude: UILabel!
    @IBOutlet weak var longitude: UILabel!
    var global_lat: String = "0.0"
    var global_long: String = "0.0"
    var x_array: [String] = []
    var y_array: [String] = []
    var z_array: [String] = []
    var lat_array: [String] = []
    var long_array: [String] = []
    
    override func viewDidLoad()
    {
        super.viewDidLoad()
        
        // Don't let iphone sleep
        UIApplication.shared.isIdleTimerDisabled = true
    
        CLmanager.desiredAccuracy = kCLLocationAccuracyBest
        CLmanager.delegate = self
        CLmanager.requestWhenInUseAuthorization()
        CLmanager.startUpdatingLocation()
        startLocation = nil

        CMmanager.gyroUpdateInterval = 0.05
        CMmanager.startGyroUpdates()
        
        Timer.scheduledTimer(timeInterval: 0.05, target: self, selector: #selector(MainViewController.gyro_update), userInfo: nil, repeats: true)
        
        Timer.scheduledTimer(timeInterval: 10, target: self, selector: #selector(MainViewController.post_data), userInfo: nil, repeats: true)

    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations:[CLLocation]) {
        latitude.text = String(locations[locations.count - 1].coordinate.latitude)
        longitude.text = String(locations[locations.count - 1].coordinate.longitude)
        global_lat = String(locations[locations.count - 1].coordinate.latitude)
        global_long = String(locations[locations.count - 1].coordinate.longitude)
    }
    
    
    
    func gyro_update()
    {
        
        if let x_data = CMmanager.gyroData?.rotationRate.x,
            let y_data = CMmanager.gyroData?.rotationRate.y,
            let z_data = CMmanager.gyroData?.rotationRate.z
        {
            x_label.text = String(x_data)
            x_array.append(String(abs(x_data)))
            y_label.text = String(y_data)
            y_array.append(String(abs(y_data)))
            z_label.text = String(z_data)
            z_array.append(String(abs(z_data)))
            lat_array.append(String(global_lat))
            long_array.append(String(global_long))
        }
        
    }
    
    func post_data(){
        print("POST CALLED")
        let url = URL(string: "http://34.205.150.122/data")!
        var request = URLRequest(url: url)
        let jsonObject: [String: [String]]  = [
            "x": x_array,
            "y": y_array,
            "z": z_array,
            "lat": lat_array,
            "long": long_array
        ]
        
        let jsonData = try! JSONSerialization.data(withJSONObject: jsonObject, options: [])
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData

        x_array.removeAll()
        y_array.removeAll()
        z_array.removeAll()
        lat_array.removeAll()
        long_array.removeAll()
        
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            guard let data = data, error == nil else {
                print("error=\(String(describing: error))")
                return
            }
            
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("statusCode should be 200, but is \(httpStatus.statusCode)")
                print("response = \(String(describing: response))")
            }
            
            let responseJSON = try? JSONSerialization.jsonObject(with: data, options: [])
            print(responseJSON as Any)
        }
        task.resume()
    }
    
}
