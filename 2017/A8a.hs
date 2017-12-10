import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set

------
iread :: String -> Int
iread = read

do2 f g x = (f x, g x)

answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

ord0 c = C.ord c - C.ord 'a'
chr0 i = C.chr (i + C.ord 'a')
incletter c i = chr0 ((ord0 c + i) `mod` 26)

splitOn1 a b = fromJust $ stripInfix a b
rsplitOn1 a b = fromJust $ stripInfixEnd a b

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

parseCmd :: String -> (Int -> Int -> Int)
parseCmd "dec" = (-)
parseCmd "inc" = (+)

parseOp :: String -> (Int -> Int -> Bool)
parseOp ">=" = (>=)
parseOp ">" = (>)
parseOp "<=" = (<=)
parseOp "<" = (<)
parseOp "==" = (==)
parseOp "!=" = (/=)

look map s = Map.findWithDefault 0 s map

exec map (ra, cmd, n, rb, op, m) =
  if look map rb `op` m then
    Map.insert ra (look map ra `cmd` n) map
    else map

parse s = let [ra, cmd, sn, _, rb, op, sm] = words s
  in (ra, parseCmd cmd, iread sn, rb, parseOp op, iread sm)


main = answer $ maximum . Map.elems . foldl exec Map.empty . map parse . lines
