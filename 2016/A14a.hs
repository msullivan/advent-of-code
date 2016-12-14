import Data.List
import Data.Maybe
import Data.Hash.MD5
import Debug.Trace

key = "yjdafjpo"

stream = map (\i -> (i, md5s $ Str $ key ++ show i)) [0..]

getTrip (a : rest@(b : c : _)) | a == b && b == c = Just a
getTrip (_ : rest) = getTrip rest
getTrip _ = Nothing

isKey ((i, x) : rest) = case getTrip x of
  Nothing -> False
  Just c -> any (isInfixOf (replicate 5 c) . snd) (take 1000 rest)

main = putStrLn $ show $ (map head $ filter isKey (tails stream)) !! 63
