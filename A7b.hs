import Data.List
import Data.Word
import Data.Maybe
import Data.Bits
import qualified Data.Char
import qualified Data.Map as Map

type Signals = Map.Map String Word16

lookupSignal :: Signals -> String -> Word16
lookupSignal signals key | any Data.Char.isAlpha key =
  case Map.lookup key signals of
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

processGate :: Signals -> Signals -> String -> Signals
processGate signals signalsPart cmd =
  let (gate, ["->", output]) = break (== "->") $ words cmd
      -- keep the old value, if there is one
  in Map.insertWith (flip const) output (computeGate gate signals) signalsPart


makeSignals :: [String] -> Signals -> Signals
makeSignals cmds start = signals
  where signals = foldl (processGate signals) start cmds

lol cmds =
  let a_val = fromJust $ Map.lookup "a" $ makeSignals cmds Map.empty
  in fromJust $ Map.lookup "a" $ makeSignals cmds (Map.singleton "b" a_val)

answer f = interact $ (++"\n") . show . f
main = answer $ lol . lines
