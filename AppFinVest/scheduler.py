from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from AppFinVest.tarefas import atualizar_precos
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    try:
        # Inicializa o scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Verifica se a tarefa já está agendada antes de adicionar
        if not scheduler.get_job("atualizar_precos"):
            # Agendando a tarefa para rodar a cada 10 minutos
            scheduler.add_job(
                atualizar_precos,
                trigger=IntervalTrigger(minutes=1),
                id="atualizar_precos",
                replace_existing=True,
            )
            logger.info("Tarefa 'atualizar_precos' agendada para rodar a cada 10 minutos.")
        else:
            logger.info("A tarefa 'atualizar_precos' já está agendada.")

        # Registra eventos para monitorar falhas
        register_events(scheduler)

        # Inicia o scheduler
        scheduler.start()
        logger.info("Agendador iniciado com sucesso.")

    except Exception as e:
        logger.error(f"Erro ao iniciar o agendador: {str(e)}")

