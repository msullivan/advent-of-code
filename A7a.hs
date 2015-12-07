import Data.List
import Data.Word
import Data.Maybe
import Data.Bits
import qualified Data.Char

--import qualified Data.Map.Lazy as Map
--type Signals = Map.Map String Word16
--doLookup = Map.lookup
--doInsert = Map.insert

-- Write a bullshit implementation of a map (based on functions) that
-- works...
type Signals = String -> Maybe Word16
doLookup key m = m key
doInsert key val map key' = if key == key' then Just val else map key'


lookupSignal :: Signals -> String -> Word16
lookupSignal signals key | any Data.Char.isAlpha key =
  case doLookup key signals of
    Just v -> v
    Nothing -> error ("couldn't lookup: " ++ key)
lookupSignal _ key  = read key



computeGate :: [String] -> Signals -> Word16
computeGate cmd signals = comp cmd
  where comp [x, "AND", y] = val x .&. val y
        comp [x, "OR",  y] = val x .|. val y
        comp [x, "LSHIFT",  y] = val x `shiftL` (fromEnum $ val y)
        comp [x, "RSHIFT",  y] = val x `shiftR` (fromEnum $ val y)
        comp ["NOT",  x] = complement $ val x
        comp [x] = val x

        val = lookupSignal signals

processGate :: Signals -> String -> Signals
processGate signals cmd =
  let (gate, ["->", output]) = break (== "->") $ words cmd
  in doInsert output (computeGate gate signals) signals


makeSignals :: [String] -> Signals
makeSignals cmds = signals
  where signals = foldl processGate signals cmds


answer f = interact $ (++"\n") . show . f
main = answer $ fromJust . doLookup "a" . makeSignals . lines
