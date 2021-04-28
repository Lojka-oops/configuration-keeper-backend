"""14_03_2021 migration_3

Revision ID: b4c0ded6354e
Revises: 98cf70e48234
Create Date: 2021-03-14 15:44:39.742681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4c0ded6354e'
down_revision = '98cf70e48234'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
            CREATE OR REPLACE FUNCTION update_environment_updated_at_time()
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE environments SET updated_at = now() WHERE id = NEW."env_id";
                RETURN NEW;   
            END;
            $$ language 'plpgsql';

            DROP TRIGGER IF EXISTS update_environment_updated_at_time_on_update_trigger ON variables;
            CREATE TRIGGER update_environment_updated_at_time_on_update_trigger BEFORE UPDATE ON variables FOR EACH ROW EXECUTE PROCEDURE update_environment_updated_at_time();
            DROP TRIGGER IF EXISTS update_environment_updated_at_time_on_create_trigger ON variables;
            CREATE TRIGGER update_environment_updated_at_time_on_create_trigger BEFORE INSERT ON variables FOR EACH ROW EXECUTE PROCEDURE update_environment_updated_at_time();   

            CREATE OR REPLACE FUNCTION update_application_updated_at_time()
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE applications SET updated_at = now() WHERE id = NEW."app_id";
                RETURN NEW;   
            END;
            $$ language 'plpgsql';

                     
            DROP TRIGGER IF EXISTS update_application_updated_at_time_on_update_trigger ON environments;
            CREATE TRIGGER update_application_updated_at_time_on_update_trigger BEFORE UPDATE ON environments FOR EACH ROW EXECUTE PROCEDURE update_application_updated_at_time();
            DROP TRIGGER IF EXISTS update_application_updated_at_time_on_create_trigger ON environments;
            CREATE TRIGGER update_application_updated_at_time_on_create_trigger BEFORE INSERT ON environments FOR EACH ROW EXECUTE PROCEDURE update_application_updated_at_time();
        '''
    )
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        '''
            DROP TRIGGER IF EXISTS update_environment_updated_at_time_on_update_trigger ON variables;
            DROP TRIGGER IF EXISTS update_environment_updated_at_time_on_create_trigger ON variables;
            DROP TRIGGER IF EXISTS update_application_updated_at_time_on_update_trigger ON environments;
            DROP TRIGGER IF EXISTS update_application_updated_at_time_on_create_trigger ON environments;
        '''
    )
    # ### end Alembic commands ###
