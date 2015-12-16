import Data.List
import Control.Monad
import Data.List.Extra
import Data.Word
import Data.Maybe
import Data.Bits
import qualified Data.Char
import qualified Data.Map as Map

type Data = Map.Map String Int

input = "Sue 0: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1"

target = snd $ readSue input

readSue :: String -> (Int, Data)
readSue s =
  let (prefix, body) = breakOn ": " s
      body' = drop 2 body
      fragments = splitOn ", " body'
      parsePart frag =
        let [key, count] = splitOn ": " frag in
        (key, read count)
      ["Sue", num] = words prefix
  in (read num, Map.fromList $ map parsePart fragments)

matches :: (Int, Data) -> Bool
matches (i, d) = all present $ Map.toList d
  where present (k, v) = Map.lookup k target == Just v

solve :: String -> Int
solve = fst . head . filter matches . map readSue . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
