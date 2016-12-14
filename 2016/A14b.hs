-- ASDF. Data.Hash.MD5 appeared to suck.

import Data.List
import qualified Crypto.Hash.MD5 as MD5
import qualified Data.ByteString.Char8 as BS
import qualified Data.ByteString.Base16 as B16
import Debug.Trace


key = "yjdafjpo"
--key = "abc"

md5' = B16.encode . MD5.hash
smd5 s = trace s (loop 2017 (BS.pack s))
  where loop 0 s = BS.unpack s
        loop k s = loop (k-1) (md5' s)

stream = map (\i -> (i, smd5 $ key ++ show i)) [0..]

getTrip (a : rest@(b : c : _)) | a == b && b == c = Just a
getTrip (_ : rest) = getTrip rest
getTrip _ = Nothing

isKey ((i, x) : rest) = case getTrip x of
  Nothing -> False
  Just c -> any (isInfixOf (replicate 5 c) . snd) (take 1000 rest)

main = putStrLn $ show $ (map head $ filter isKey (tails stream)) !! 63
