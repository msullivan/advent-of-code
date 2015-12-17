import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map

type Distances = Map.Map (String, String) Int

parseLine :: String -> [((String, String), Int)]
parseLine s =
  let [loc1, "to", loc2, "=", num] = words s
      dist = read num
  in
   [((loc1, loc2), dist), ((loc2, loc1), dist)]

makeMap :: [String] -> Distances
makeMap = Map.fromList . concatMap parseLine

adjPairs :: [a] -> [(a, a)]
adjPairs xs = zip xs (tail xs)

findShortest :: Distances -> Int
findShortest ds = minimum $ map pathCost $ permutations cities
  where cities = nub $ map fst $ Map.keys ds
        get k = fromJust $ Map.lookup k ds
        pathCost l = sum $ map get $ adjPairs l

solve :: String -> Int
solve = findShortest . makeMap . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
