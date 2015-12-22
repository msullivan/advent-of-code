-- This solution is totally rubbish. It doesn't output the minimum
-- solution, it outputs the first solution that it sees. This somehow
-- happens to work. I should maybe /actually/ solve this problem.

-- Aha. Comments from the AOC create indicate that the grammar is
-- actually unamibiguous (at least in terms of how many rules
-- fire). This means that finding the first solution /is/ correct
-- (though I didn't know it, of course). Now, this solution also
-- doesn't actually manage to find the right solution for any *good*
-- reason. The order that I generated candidates just happened to work
-- on my input in a (very short) reasonable amount of time. It also
-- seems to work on some other inputs I got my hands on.

-- I flip the rules and work backwards from the molecule to e.  What
-- it winds up doing, I think is always applying the rule that applies
-- to the rightmost part of the string. And this seems to actually
-- just work greedily on the inputs I've tried. Huh.

import Control.Monad
import Data.List.Extra
import Data.Maybe
--import Data.Function.Memoize
--import Memoize
import Data.Function
import qualified Data.Char
import qualified Data.Map as Map
import Debug.Trace

splitOn1 a b = fromJust $ stripInfix a b

type Mappings = [(String, String)]

getMappings :: String -> Mappings -> [String]
getMappings s = map snd . filter (\(x, _) -> x == s)

getMap s = (to, from) -- Reverse the transformation, search backwards
  where [from, "=>", to] = words s

checkMatch :: String -> (String, String) -> Maybe (String, String)
checkMatch s (from, to) =
  case stripPrefix from s of
    Nothing -> Nothing
    Just post -> Just (to, post)

getNuses mapping [] = []
getNuses mapping (x:xs) =
  map (x:) (getNuses mapping xs) ++
  do (to, post) <- mapMaybe (checkMatch (x:xs)) mapping
     return $ to++post


infty = 1000000000000000000000000000000000
-- XXX: This is rubbish, and wrong. We really need to take the
-- /minimum/. But that was too slow, even when we memoized, and taking
-- the /first/ somehow produced the right answer. If we reverse the
-- results from getNuses, it no longer does. Looool.
getCost :: [Integer] -> Integer
getCost x = case filter (<infty) x of
  [] -> infty
  a : as -> a

findMin :: Mappings -> String -> Integer
findMin mapping = {-memoFix-}fix search
  where search _ "e" = 0
        search search' s =
          1 + (getCost $ do
            s' <- getNuses mapping s
            return $ search' s')


solve input = findMin mappings molecule
  where molecule : "" : smappings = reverse $ lines input
        mappings = map getMap smappings

answer f = interact $ (++"\n") . show . f
main = answer solve
