import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char
import qualified Data.Map as Map

splitOn1 a b = fromJust $ stripInfix a b

--type Data = Map.Map String Int
type Mappings = [(String, String)]

getMappings :: String -> Mappings -> [String]
getMappings s = map snd . filter (\(x, _) -> x == s)

getMap s = (from, to)
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


solve input = length $ nub $ getNuses mappings molecule
  where molecule : "" : smappings = reverse $ lines input
        mappings = map getMap smappings

answer f = interact $ (++"\n") . show . f
main = answer solve
