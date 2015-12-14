import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map

type Distances = Map.Map (String, String) Int

parseLine :: String -> [((String, String), Int)]
parseLine s =
  let [loc1, "would", dir, num, _, _, _, _, _, _, loc2] = words $ filter (/='.') s
      mult = if dir == "gain" then 1 else -1
      dist = read num * mult
  in
   [((loc1, loc2), dist)]

makeMap :: [String] -> Distances
makeMap = Map.fromList . concatMap parseLine

adjPairs :: [a] -> [(a, a)]
adjPairs (a1 : a2 : as) = (a1, a2) : adjPairs (a2 : as)
adjPairs _ = []

lolpairs xs = (last xs, head xs) : adjPairs xs

findShortest :: Distances -> Int
findShortest ds = maximum costs
  where cities = "me" : (nub $ map fst $ Map.keys ds)
        lists = map lolpairs $ permutations cities
        get (k1, k2) | k1 == "me" || k2 == "me" = 0
                     | otherwise = (fromJust $ Map.lookup (k1, k2) ds) +
                                   (fromJust $ Map.lookup (k2, k1) ds)
        listcost l = sum $ map get l
        costs = map listcost lists

solve :: String -> Int
solve = findShortest . makeMap . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
