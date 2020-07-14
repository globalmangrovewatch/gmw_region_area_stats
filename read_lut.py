import json

with open('gadm_lut.json') as f:
    lut = json.load(f)
    gid_lut = lut["gid"]
    ctry_lut = lut["ctry"]
    
print(gid_lut["MNP"]) # Will print 'Northern Mariana Islands'
print(ctry_lut["Vietnam"]) # Will print 'VNM'

