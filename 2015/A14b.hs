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

totalDistance :: [Int] -> [Int]
totalDistance = tail . scanl (+) 0

leadingDistance :: [[Int]] -> [Int]
leadingDistance = map maximum . transpose

currentScore :: [Int] -> [Int] -> [Int]
currentScore =
  zipWith (\lead x -> if lead == x then 1 else 0)

time = 2503
furthest :: [[Int]] -> Int
furthest speeds = maximum $ map (sum . take time) scores

  where leader = leadingDistance totals
        totals = map totalDistance speeds
        scores = map (currentScore leader) totals



solve :: String -> Int
solve = furthest . allDistances . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
