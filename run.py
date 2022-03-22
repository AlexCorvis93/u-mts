from flask_migrate import Migrate
from app import app
from app.models import Proposal, db, Product, ProductImage, CompletedProposal
from flask.cli import FlaskGroup

cli = FlaskGroup(app)


def make_shell_context():
    return dict(app=app, db=db, Proposal=Proposal, Product=Product, ProductImage=ProductImage, CompletedProposal=CompletedProposal )


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()