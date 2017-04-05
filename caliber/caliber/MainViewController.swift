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
    var global_lat: Double = 0.0
    var global_long: Double = 0.0
    var x_array: [Double] = []
    var y_array: [Double] = []
    var z_array: [Double] = []
    var lat_array: [Double] = []
    var long_array: [Double] = []
    
    override func viewDidLoad()
    {
        super.viewDidLoad()
    
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
        global_lat = locations[locations.count - 1].coordinate.latitude
        global_long = locations[locations.count - 1].coordinate.longitude
    }
    
    
    
    func gyro_update()
    {
        
        if let x_data = CMmanager.gyroData?.rotationRate.x {
            x_label.text = String(x_data)
            x_array.append(x_data)
        }
        if let y_data = CMmanager.gyroData?.rotationRate.y {
            y_label.text = String(y_data)
            y_array.append(y_data)
        }
        if let z_data = CMmanager.gyroData?.rotationRate.z {
            z_label.text = String(z_data)
            z_array.append(z_data)
        }
        
        lat_array.append(global_lat)
        long_array.append(global_long)
        
    }
    
    func post_data(){
        print("POST CALLED")
        let url = URL(string: "http://34.205.150.122/data")!
        var request = URLRequest(url: url)
        let jsonObject: [String: [Double]]  = [
            "x_data": x_array,
            "y_data": y_array,
            "z_data": z_array,
            "lat_data": lat_array,
            "long_data": long_array
        ]
        
        let jsonData = try! JSONSerialization.data(withJSONObject: jsonObject, options: [])
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        print(x_array)
        print(x_array.count)
        x_array.removeAll()

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
