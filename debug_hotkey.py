from dahora_app.hotkey_validator import HotkeyValidator

hotkey = 'ctrl+a'
normalized = HotkeyValidator.normalize(hotkey)
mods, key = HotkeyValidator.parse(normalized)

print(f"Hotkey: {hotkey}")
print(f"Normalized: {normalized}")
print(f"Mods: {mods}, Key: {key}")
print(f"Is key valid: {HotkeyValidator._is_valid_key(key)}")
print(f"Key type: {type(key)}, repr: {repr(key)}")
print(f"Key in RESERVED: {normalized in HotkeyValidator.RESERVED_HOTKEYS}")
print(f"Key in BLOCKED: {key in HotkeyValidator.BLOCKED_KEYS}")

# Step by step
print("\nStep by step:")
print(f"1. Mods check: {bool(mods)} and {bool(key)}")
print(f"2. Mod validity: {all(m in HotkeyValidator.VALID_MODIFIERS for m in mods)}")
print(f"3. Key validity: {HotkeyValidator._is_valid_key(key)}")
print(f"4. Blocked key: {key in HotkeyValidator.BLOCKED_KEYS}")

print(f"\nFinal is_valid: {HotkeyValidator.is_valid('ctrl+a')}")
