from app.database.database import SessionLocal

from app.database.models import (
    AtivoModel,
    ContaModel,
    InvestidorModel,
    PosicaoCarteiraModel
)

from app.security.password import gerar_hash_senha


def popular_banco():
    db = SessionLocal()

    try:
        investidor = (
            db.query(InvestidorModel)
            .filter_by(
                email="gabriel@sentineltrade.com"
            )
            .first()
        )

        senha_hash = gerar_hash_senha(
            "Sentinel123"
        )

        if investidor is None:
            investidor = InvestidorModel(
                nome="Gabriel",
                email="gabriel@sentineltrade.com",
                senha_hash=senha_hash,
                mfa_habilitado=True,
                status="ativo"
            )

            db.add(investidor)
            db.commit()
            db.refresh(investidor)

        else:
            investidor.senha_hash = senha_hash
            investidor.mfa_habilitado = True
            investidor.status = "ativo"

            db.commit()
            db.refresh(investidor)

        conta = (
            db.query(ContaModel)
            .filter_by(
                investidor_id=investidor.id
            )
            .first()
        )

        if conta is None:
            conta = ContaModel(
                investidor_id=investidor.id,
                saldo_disponivel=50000.00,
                limite_risco=20000.00,
                situacao="ativa"
            )

            db.add(conta)
            db.commit()
            db.refresh(conta)

        ativo = (
            db.query(AtivoModel)
            .filter_by(
                codigo="PETR4"
            )
            .first()
        )

        if ativo is None:
            ativo = AtivoModel(
                codigo="PETR4",
                nome="Petrobras PN",
                tipo="acao",
                cotacao=38.50
            )

            db.add(ativo)
            db.commit()

        posicao = (
            db.query(PosicaoCarteiraModel)
            .filter_by(
                conta_id=conta.id,
                codigo_ativo="PETR4"
            )
            .first()
        )

        if posicao is None:
            posicao = PosicaoCarteiraModel(
                conta_id=conta.id,
                codigo_ativo="PETR4",
                quantidade=100,
                quantidade_disponivel=100
            )

            db.add(posicao)
            db.commit()

        print(
            "Banco populado com sucesso."
        )

        print(
            f"ID do investidor: {investidor.id}"
        )

        print(
            f"ID da conta: {conta.id}"
        )

        print(
            "Login de teste: "
            "gabriel@sentineltrade.com"
        )

        print(
            "Senha de teste: Sentinel123"
        )

    finally:
        db.close()


if __name__ == "__main__":
    popular_banco()