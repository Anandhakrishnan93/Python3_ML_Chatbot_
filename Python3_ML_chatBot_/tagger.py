import string

class Tagger:
   previousTag = {}
   def __init__(self):
        self.places = ["Delhi", "Mumbai", "Hyderabad", "Bangalore", "Chennai", "Kolkata"]
        self.modes = ["Bus", "Train"]
        
   def splitTags(self, question):
        # Clean punctuation and normalize case
        clean_q = question.translate(str.maketrans('', '', string.punctuation)).lower()
        words = clean_q.split()

        # Find which tags exist in the question
        found_place = next((p for p in self.places if p.lower() in words), None)
        found_mode = next((m for m in self.modes if m.lower() in words), None)
        return {"mode": found_mode, "place": found_place}
   
   def process(self,user_input):
       # 1. Extract what the user just said
        new_tags = self.splitTags(user_input)

        # 2. Context Merging Logic
        # If the user mentioned a NEW place/mode, update context.
        # If they didn't mention it, keep the old one from memory.
        # This takes the new value if it exists, otherwise it keeps the old one
        old_place = new_tags["place"]
        old_mode = new_tags["mode"]
        new_tags["place"] = new_tags["place"] or self.previousTag.get("place")
        new_tags["mode"] = new_tags["mode"] or self.previousTag.get("mode")

        self.previousTag = new_tags
        new_sentence = ""
        if old_place is None:
           new_sentence = user_input + new_tags["place"]
        else:
           new_sentence = user_input.replace(old_place,  new_tags["place"]) 
   
        if old_mode is None:
           new_sentence = new_sentence + new_tags["mode"]
        else:
           new_sentence = new_sentence.replace(old_mode,  new_tags["mode"]) 
        return new_sentence
