import fs from 'fs';
import path from 'path';

// Получи токен на https://huggingface.co/settings/tokens (бесплатно, тип "Read")
const HF_TOKEN = process.env.HUGGINGFACE_TOKEN;
if (!HF_TOKEN) {
    console.error('❌ Установи переменную окружения: export HUGGINGFACE_TOKEN="hf_..."');
    process.exit(1);
}

const MODEL = 'mistralai/Mistral-7B-Instruct-v0.3';
const API_URL = `https://api-inference.huggingface.co/models/${MODEL}`;

const LEVELS_CONFIG = {
    A0: ['Greetings', 'Numbers', 'Colors', 'Family', 'Food', 'Animals', 'Daily Objects', 'Simple Verbs'],
    A1: ['Daily Routine', 'Shopping', 'Weather', 'Hobbies', 'Transport', 'Clothes', 'Body Parts', 'Time'],
    A2: ['Travel', 'Health', 'Work', 'Technology', 'Environment', 'Feelings', 'Past Events', 'Future Plans'],
    B1: ['Culture', 'Education', 'Career', 'Relationships', 'Media', 'Science', 'Debate', 'Opinions'],
    B2: ['Global Issues', 'Psychology', 'Economics', 'Arts', 'Ethics', 'Innovation', 'Abstract Concepts', 'Complex Grammar']
};

const LESSONS_PER_TOPIC = 3; // Сколько уроков генерировать на тему за запуск
const OUTPUT_FILE = 'lessons.json';

async function callHF(prompt, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const res = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${HF_TOKEN}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    inputs: prompt,
                    parameters: {
                        max_new_tokens: 1500,
                        temperature: 0.2,
                        do_sample: true,
                        return_full_text: false
                    }
                })
            });

            if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
            const data = await res.json();
            if (data.error) throw new Error(data.error);
            return data[0].generated_text;
        } catch (err) {
            console.warn(`⚠️ Attempt ${i+1} failed: ${err.message}`);
            await new Promise(r => setTimeout(r, 8000 * (i+1)));
        }
    }
    throw new Error('Failed after retries');
}

async function generateLesson(level, topic, num) {
    const prompt = `
You are an expert English teacher. Generate a lesson for ${level} level on topic "${topic}".
Return ONLY valid JSON. No markdown, no explanations.
Schema:
{
  "id": "${level}_L${num}",
  "title": "Урок ${num}: ${topic}",
  "theory": ["Step 1 (intro)", "Step 2 (rules/examples)", "Step 3 (tips)"],
  "questions": [
    {"q": "Question 1?", "a": ["A", "B", "C", "D"], "c": 0},
    ... 19 more
  ]
}
Rules:
- Exactly 20 questions. "c" is index 0-3 of correct answer.
- Mix vocabulary and grammar appropriate for ${level}.
- Keep text concise. Explanations in Russian, examples in English.
`;

    const raw = await callHF(prompt);
    const match = raw.match(/\{[\s\S]*\}/);
    if (!match) throw new Error('No JSON found');
    
    const lesson = JSON.parse(match[0]);
    if (!lesson.id || !lesson.theory || !lesson.questions || lesson.questions.length !== 20) {
        throw new Error('Invalid structure');
    }
    return lesson;
}

async function main() {
    let db = fs.existsSync(OUTPUT_FILE) ? JSON.parse(fs.readFileSync(OUTPUT_FILE, 'utf8')) : {};
    
    for (const [level, topics] of Object.entries(LEVELS_CONFIG)) {
        console.log(`\n📚 Level: ${level}`);
        if (!db[level]) db[level] = [];
        
        for (let t = 0; t < topics.length; t++) {
            const topic = topics[t];
            console.log(`  📝 Topic: ${topic}`);
            
            for (let l = 0; l < LESSONS_PER_TOPIC; l++) {
                const num = t * LESSONS_PER_TOPIC + l + 1;
                if (db[level].find(x => x.id === `${level}_L${num}`)) continue;

                try {
                    console.log(`    ⏳ Generating ${level}_L${num}...`);
                    const lesson = await generateLesson(level, topic, num);
                    db[level].push(lesson);
                    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(db, null, 2));
                    console.log(`    ✅ Saved`);
                    await new Promise(r => setTimeout(r, 12000)); // Free tier delay
                } catch (err) {
                    console.error(`    ❌ Skipped: ${err.message}`);
                }
            }
        }
    }
    console.log('\n🎉 Done! Check lessons.json');
}

main();
