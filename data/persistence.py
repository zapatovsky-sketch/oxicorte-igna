import pandas as pd
import datetime

def calculate_next_review(performance_score):
    """
    Determina cuántos días deben pasar para repetir una pregunta.
    performance_score: 1 (Mal) a 5 (Excelente)
    """
    intervals = {
        1: 0,   # Repetir de inmediato (misma sesión)
        2: 1,   # Repetir mañana
        3: 3,   # Repetir en 3 días
        4: 7,   # Repetir en una semana
        5: 30   # Pregunta dominada
    }
    days_to_add = intervals.get(performance_score, 0)
    return datetime.date.today() + datetime.timedelta(days=days_to_add)

def update_student_progress(conn, student_id, question_id, score):
    """
    Registra el desempeño en la base de datos cloud.
    """
    next_date = calculate_next_review(score)
    
    # Preparamos el registro de progreso
    new_data = pd.DataFrame([{
        "student_id": student_id,
        "question_id": question_id,
        "last_score": score,
        "last_seen": datetime.date.today(),
        "next_review": next_date
    }])
    
    # Aquí el motor de engine.py usaría la conexión para hacer un 'append' 
    # en la pestaña "Progreso" de tu Google Sheets.
    # conn.create(data=new_data, worksheet="Progreso") 
    
    return next_date

def filter_questions_by_memory(questions_df, progress_df):
    """
    Cruza el banco de preguntas con el progreso de Ignacia para
    devolver solo las que toca revisar hoy.
    """
    if progress_df.empty:
        return questions_df
        
    today = datetime.date.today()
    
    # Unimos para identificar preguntas que ya tienen fecha de revisión
    merged = pd.merge(questions_df, progress_df, left_on='id', right_on='question_id', how='left')
    
    # Prioridad: Preguntas nuevas (NaN) o preguntas cuya fecha de revisión sea <= hoy
    to_review = merged[
        (merged['next_review'].isna()) | 
        (pd.to_datetime(merged['next_review']).dt.date <= today)
    ]
    
    return to_review.drop(columns=['question_id', 'last_score', 'last_seen', 'next_review'], errors='ignore')