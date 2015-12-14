import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map


parseLine :: String -> [Int]
parseLine s =
  let [name, _, _, speed, "km/s", _, endurance, "seconds,",
        _, _, _, _, _, rest, "seconds."] = words s
  in
   concat $ repeat $ replicate (read endurance) (read speed) ++ replicate (read rest) 0

allDistances :: [String] -> [[Int]]
allDistances = map parseLine

totalDistance :: Int -> [Int] -> Int
totalDistance time thingus = sum $ take time thingus


time = 2503
furthest :: [[Int]] -> Int
furthest dists = maximum $ map (totalDistance time) dists


solve :: String -> Int
solve = furthest . allDistances . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
