import Data.List
import Control.Monad
import Data.List.Extra
import Data.Word
import Data.Maybe
import Data.Bits
import qualified Data.Char
import qualified Data.Map as Map


datas = [[2, 0, -2, 0, 3],
         [0, 5, -3, 0, 3],
         [0, 0, 5, -1, 8],
         [0, -1, 0, 5, 8]]

notcalories = map (take 4) datas

crap count 1 = [[count]]
crap count n =
  do k <- [0..count]
     l <- crap (count-k) (n-1)
     return (k : l)

scale k l = map (* k) l

asdf =
  do vec <- crap 100 (length notcalories)
     let nus = zipWith scale vec notcalories
         butts = map sum $ transpose nus
     guard $ not (any (<0) butts)
     return $ product butts

main = putStrLn $ show $ maximum asdf
