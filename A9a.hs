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
adjPairs (a1 : a2 : as) = (a1, a2) : adjPairs (a2 : as)
adjPairs _ = []

findShortest :: Distances -> Int
findShortest ds = minimum costs
  where cities = nub $ map fst $ Map.keys ds
        lists = map adjPairs $ permutations cities
        get k = fromJust $ Map.lookup k ds
        listcost l = sum $ map get l
        costs = map listcost lists

solve :: String -> Int
solve = findShortest . makeMap . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
