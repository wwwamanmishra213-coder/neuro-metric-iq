with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """      generateFinalClinicalReport() {
        clearInterval(this.state.timerInterval);
        clearInterval(this.state.itemElapsedInterval);

        document.getElementById('screenWorkspace').classList.add('hidden');
        document.getElementById('screenReport').classList.remove('hidden');"""

replacement = """      generateFinalClinicalReport() {
        clearInterval(this.state.timerInterval);
        clearInterval(this.state.itemElapsedInterval);

        showScreen('screenReport');"""

target_norm = target.replace('\r\n', '\n')
replacement_norm = replacement.replace('\r\n', '\n')
text_norm = text.replace('\r\n', '\n')

if target_norm in text_norm:
    text_norm = text_norm.replace(target_norm, replacement_norm, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text_norm)
    print("generateFinalClinicalReport updated to use showScreen('screenReport')!")
else:
    print("Error: target_norm not found!")
