#!/usr/bin/env python3
import os
import re
import random
import json

# --- Flavor Text Pools ---
FLAVOR_D0 = [
    "You roll a smooth sphere. It never stops rolling.",
    "A black hole forms on the table.",
    "Error 404: Geometry not found.",
    "You roll a 0-sided die. Nothing happens. Forever."
]

FLAVOR_0_DICE = [
    "You reach into your bag, pull out absolutely nothing, and roll it. You get a nothing.",
    "0 dice rolled. 0 energy expended. 0 fun.",
    "You roll 0 dice. The ghost of a natural 20 haunts you.",
    "Nothing rolls across the table. It's a very quiet game night.",
    "Are you trying to save on virtual plastic?"
]

FLAVOR_D1 = [
    "Really?",
    "You know the answer is going to be the same each time, right?",
    "Let me add up those ones for you...",
    "Ah, the illusion of choice.",
    "Suspenseful... oh wait, it's exactly what you thought."
]

FLAVOR_CRIT_FAIL = [
    "Oof. Critical failure!",
    "A 1. You trip over your own feet.",
    "Nat 1! The dice gods frown upon you.",
    "Critical miss! Please try again when you have better luck."
]

FLAVOR_CRIT_SUCCESS = [
    "Nat 20! Critical success!",
    "A 20! You do it with effortless style.",
    "Critical hit! The crowd goes wild.",
    "20! Absolutely flawless."
]

FLAVOR_FIREBALL = [
    "FIREBALL!",
    "How many party members are caught in the blast?",
    "I didn't ask how big the room is, I said I cast Fireball.",
    "Smells like burning goblins."
]

FLAVOR_GENERIC = [
    "You rolled",
    "That's a",
    "Dramatic pause...",
    "The dice say",
    "Result:",
    "Fate decrees:"
]

# 8-Ball Prefixes (Updated to flow naturally into lowercase responses)
FLAVOR_8BALL_PREFIXES = [
    "The magic 8-ball says...",
    "You shake the plastic sphere and it reveals...",
    "The spirits whisper...",
    "I wouldn't trust it, but the 8-ball says...",
    "Gazing into the dark fluid, you see...",
    "The oracle has spoken...",
    "After much shaking, the answer appears...",
    "The glowing triangle floats up and reads...",
    "You consult the arcane tome, finding the words...",
    "Through the static of the mesh, a message arrives...",
    "The GM smiles cryptically and says..."
]

FLAVOR_8BALL = [
    # Classics
    "it is certain.", "it is decidedly so.", "without a doubt.",
    "yes, definitely.", "you may rely on it.", "as I see it, yes.",
    "most likely.", "outlook good.", "yes.", "signs point to yes.",
    "reply hazy, try again.", "ask again later.", "better not tell you now.",
    "cannot predict now.", "concentrate and ask again.",
    "don't count on it.", "my reply is no.", "my sources say no.",
    "outlook not so good.", "very doubtful.",
    # Humorous additions
    "have you tried turning it off and on again?",
    "the spirits are on break, try later.",
    "outlook not so good, much like your fashion sense.",
    "in this economy? absolutely not.",
    "I'm just a script, don't put this pressure on me."
]

def process_command(command_str):
    output = ""
    
    # 0. Help Logic
    if "help" in command_str:
        return "Usage: /roll <NdM>[+|-K] [adv|dis]. Examples: '1d20', '2d6+4', '1d20 adv'. Special commands: 'coinflip', '8ball'."

    # 1. Coinflip Logic
    elif "coinflip" in command_str:
        output = random.choice(["Heads", "Tails"])
        
    # 2. 8-Ball Logic
    elif "8ball" in command_str:
        prefix = random.choice(FLAVOR_8BALL_PREFIXES)
        answer = random.choice(FLAVOR_8BALL)
        output = f"{prefix} {answer}"

    # 3. Dice Parsing Logic
    else:
        match = re.search(r'(\d+)\s*d\s*(\d+)(?:\s*([+-])\s*(\d+))?(?:\s*(adv|dis|advantage|disadvantage))?', command_str)
        if not match:
            return "Invalid command or roll format. Try '/roll help' for some insight."

        num_dice = int(match.group(1))
        sides = int(match.group(2))
        
        if num_dice > 10000:
            return "Limit exceeded. Try fewer dice."
            
        sign = match.group(3)
        modifier = int(match.group(4)) if match.group(4) else 0
        if sign == '-':
            modifier = -modifier
            
        adv_dis = match.group(5)

        # Check for 0 dice
        if num_dice == 0:
            output = random.choice(FLAVOR_0_DICE)
        # Check for impossible geometry (d0)
        elif sides == 0:
            output = random.choice(FLAVOR_D0)
        else:
            # Generate rolls
            if adv_dis:
                batch1 = [random.randint(1, sides) for _ in range(num_dice)]
                batch2 = [random.randint(1, sides) for _ in range(num_dice)]
                sum1 = sum(batch1)
                sum2 = sum(batch2)
                
                is_adv = adv_dis.startswith('adv')
                if is_adv:
                    rolls = batch1 if sum1 >= sum2 else batch2
                    dropped = batch1 if sum1 < sum2 else batch2
                else:
                    rolls = batch1 if sum1 <= sum2 else batch2
                    dropped = batch1 if sum1 > sum2 else batch2
                total = sum(rolls) + modifier
            else:
                rolls = [random.randint(1, sides) for _ in range(num_dice)]
                total = sum(rolls) + modifier
                dropped = None

            # Determine standard prefix
            prefix = f"{random.choice(FLAVOR_GENERIC)} {total}!"
            
            # Override prefix for specific humorous scenarios
            if sides == 1:
                prefix = f"{random.choice(FLAVOR_D1)} You rolled a {total}."
            elif num_dice == 1 and sides == 20:
                # Check the raw roll (ignoring modifier) for criticals
                if rolls[0] == 1:
                    prefix = f"{random.choice(FLAVOR_CRIT_FAIL)} (Total: {total})"
                elif rolls[0] == 20:
                    prefix = f"{random.choice(FLAVOR_CRIT_SUCCESS)} (Total: {total})"
            elif num_dice == 8 and sides == 6:
                prefix = f"{random.choice(FLAVOR_FIREBALL)} (Total damage: {total})"

            # Format final output for dice
            if adv_dis:
                adv_str = "Advantage" if adv_dis.startswith('adv') else "Disadvantage"
                rolls_str = " ".join(map(str, rolls))
                dropped_str = " ".join(map(str, dropped))
                output = f"{prefix} [{adv_str}] (Kept: {rolls_str} | Dropped: {dropped_str})"
            else:
                if num_dice == 1 and modifier == 0:
                    output = prefix
                else:
                    rolls_str = " ".join(map(str, rolls))
                    output = f"{prefix} ({rolls_str})"

    # Final safety check: Truncate strictly to 200 chars for MeshMonitor safety
    if len(output) > 200:
        output = output[:196] + "...)"

    return output

def main():
    # 1. Try to get the actual user message
    raw_cmd = os.environ.get("MESSAGE", "").lower()
    
    # 2. Fallback to the trigger pattern
    if not raw_cmd:
        raw_cmd = os.environ.get("TRIGGER", "").lower()
        
    # 3. Fallback for manual terminal testing (so you can still run `./roll.py 1d20` locally)
    if not raw_cmd:
        import sys
        raw_cmd = " ".join(sys.argv[1:]).lower()

    if not raw_cmd.strip():
        result_text = "No command provided. Try '/roll help' for some insight."
    else:
        result_text = process_command(raw_cmd)
        
    print(json.dumps({"response": result_text}))

if __name__ == "__main__":
    main()