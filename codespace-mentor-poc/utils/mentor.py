def mentor_reply(user_text: str, lesson) -> tuple[str, str, list]:
    t = user_text.lower().strip()

    if "variable" in t:
        actions = [{"type": "SHOW_LESSON", "lesson_id": "py-vars-01"}]
        reply = "A variable is a name that points to a value. Let's start with the Variables lesson."
        voice = "Variables are names for values. Let's begin."
        return reply, voice, actions

    if "function" in t:
        actions = [{"type": "SHOW_LESSON", "lesson_id": "py-func-01"}]
        reply = "Functions package logic for reuse. They usually return values."
        voice = "Functions help organize logic and return values."
        return reply, voice, actions

    actions = [{"type": "SHOW_LESSON", "lesson_id": lesson['id']}]
    reply = "Let's continue with the current lesson. Try the next exercise."
    voice = "Let's continue."
    return reply, voice, actions
