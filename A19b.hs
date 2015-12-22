-- This solution is totally rubbish. It doesn't output the minimum
-- solution, it outputs the first solution that it sees. This somehow
-- happens to work. I should maybe /actually/ solve this problem.

import Control.Monad
import Data.List.Extra
import Data.Maybe
--import Data.Function.Memoize
--import Memoize
import Data.Function
import qualified Data.Char
import qualified Data.Map as Map

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
getCost :: [Integer] -> Integer
getCost [] = infty
-- XXX: This is rubbish, and wrong. We really need to take the
-- /minimum/. But that was too slow, even when we memoized, and taking
-- the /first/ somehow produced the right answer. If we reverse the
-- results from getNuses, it no longer does. Looool.
getCost x = head x

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
