import Foundation
typealias PointTuple = (day: Double, mW: Double)

let x1:[Double] = [0.0,
                 1.0,
                 2.0,
                 4.0,
                 6.0]
let y2:[Double] = [31.98,
                 31.89,
                 31.77,
                 31.58,
                 31.46]

let x:[Double] = [
438.0
,471
,487
,504
,520
,651
]

let y:[Double] = [
17568
,20827
,21627
,20534
,18653
,194
]

var points: [PointTuple] = []

for i in 0 ..< x.count{
    points.append( (x[i], y[i]) )
}

//  The days are the values on the x-axis.
//  mW is the value on the y-axis.
/*
let points: [PointTuple] = [(0.0, 31.98),
                            (1.0, 31.89),
                            (2.0, 31.77),
                            (4.0, 31.58),
                            (6.0, 31.46)]
*/
func findBestFit(_ x:[Double], _ y:[Double]) -> (Double,Double){
    // When using reduce, $0 is the current total.
    let meanDays = points.reduce(0) { $0 + $1.day } / Double(points.count)
    let meanMW   = points.reduce(0) { $0 + $1.mW  } / Double(points.count)

    let a = points.reduce(0) { $0 + ($1.day - meanDays) * ($1.mW - meanMW) }
    let b = points.reduce(0) { $0 + pow($1.day - meanDays, 2) }

    // The equation of a straight line is: y = mx + c
    // Where m is the gradient and c is the y intercept.
    let m = a / b
    let c = meanMW - m * meanDays
    return (m,c)
}
func CalculateNextValue(_ x: Double,_ m:Double,_ c:Double) -> Double {
    return m * x + c
}

var (m,c) = findBestFit(x,y)
print( "m:\(m) c:\(c)")

print( CalculateNextValue(3, m, c) ) // 31.70
print( CalculateNextValue(5, m, c) ) // 31.52
print( CalculateNextValue(7, m, c) )// 31.35

print(m)
