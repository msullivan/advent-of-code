import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char
import qualified Data.Map as Map

splitOn1 a b = fromJust $ stripInfix a b

type Data = Map.Map String Int

input = "Sue 0: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1"

target = snd $ readSue input

readSue :: String -> (Int, Data)
readSue s =
  let (prefix, body) = splitOn1 ": " s
      fragments = splitOn ", " body
      parsePart frag =
        let (key, count) = splitOn1 ": " frag in
        (key, read count)
      ["Sue", num] = words prefix
  in (read num, Map.fromList $ map parsePart fragments)

matches :: (Int, Data) -> Bool
matches (i, d) = all present $ Map.toList d
  where lookup k = fromJust $ Map.lookup k target
        present (k@"cats", v) = lookup k < v
        present (k@"trees", v) = lookup k < v
        present (k@"pomeranians", v) = lookup k > v
        present (k@"goldfish", v) = lookup k > v

        present (k, v) = lookup k == v

solve :: String -> Int
solve = fst . head . filter matches . map readSue . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
