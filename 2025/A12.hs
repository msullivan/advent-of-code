import Control.Monad
import Data.List
import Data.List.Split
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set
import Debug.Trace

------
answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f


-- pull out every part of a String that can be read in
-- for some Read a and ignore the rest
readOut :: Read a => String -> [a]
readOut "" = []
readOut s = case reads s of
  [] -> readOut $ tail s
  [(x, s')] -> x : readOut s'
  _ -> error "ambiguous parse"
ireadOut :: String -> [Int]
ireadOut = readOut

--------

droplast l = take (length l - 1) l

rotate = transpose . map reverse

parse lines = (shapes, rules)
  where
    chunks = splitOn [[]] lines
    shapes = map tail $ droplast chunks
    rules = map ((\(x:y:rest) -> ((x, y), rest)) . ireadOut) (last chunks)

-- check whether there are enough spaces to do it
-- this obviously isn't sound in general!!
ok shapes ((w, h), cnts) =
  w * h >= sum (zipWith (*) shapes cnts)


solve (shapes, rules) = length $ filter (ok shapes') rules
  where shapes' = map (length . filter (=='#') . concat) shapes

main = answer $ solve . parse . lines
