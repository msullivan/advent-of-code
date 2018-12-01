{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE RecursiveDo #-}
{-# LANGUAGE FlexibleContexts #-}

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

import Text.Earley
import Control.Applicative

splitOn1 a b = fromJust $ stripInfix a b

type Chem = String
type CString = [Chem]

--type Mappings = [(CString, Chem)]

toChems :: String -> CString
toChems = groupBy (\x y -> Data.Char.isLower y)

--getMappings :: CString -> Mappings -> [CString]
getMappings l s = map fst $ filter (\(_, x) -> x == s) l

getMap s = (toChems to, head $ toChems from)
  where [from, "=>", to] = words s

type MappingGroup = (Chem, [CString])
type Mappings = [MappingGroup]

load :: String -> ([(Chem, [CString])], CString)
load input = (mappings', molecule) --findMin mappings molecule
  where molecule = toChems molecule'
        molecule' : "" : smappings = reverse $ lines input
        mappings = map getMap smappings
        mappings' = zip productions $ map (getMappings mappings) productions
        productions = nub $ map snd mappings

get l d x = fromMaybe d $ lookup x l

anyOf :: (Alternative f, Foldable t) => t (f a) -> f a
anyOf = foldr (<|>) empty

piece :: [(Chem, Prod r String Chem Int)]
      -> MappingGroup
      -> Grammar r (Chem, Prod r String Chem Int)
piece table (chem, productions) =
  do p <- rule mainprod
     return (chem, p)

  where mainprod = ((+1) <$> anyOf (map prod productions)) <|> nonterm chem
        lookup x = get table (nonterm x) x
        prod cs = sum <$> traverse lookup cs
        nonterm c = pure 0 <* token c

dyngrammer :: Mappings -> Chem -> Grammar r (Prod r String Chem Int)
dyngrammer mappings c = mdo
  table <- mapM (piece table) mappings
  return $ get table empty c



answer f = interact $ (++"\n") . show . f
main = answer load
