from faraday.server.models import (
    db,
    Host,
)
from faraday.server.api.modules.bulk_create import bulk_create

host_data = {
    "ip": "127.0.0.1",
    "description": "test",
    "hostnames": ["test.com", "test2.org"]
}


def test_create_host(session, workspace):
    assert Host.query.filter(Host.workspace == workspace).count() == 0
    bulk_create(workspace, dict(hosts=[host_data]))
    db.session.commit()
    host = Host.query.filter(Host.workspace == workspace).one()
    assert host.ip == "127.0.0.1"
    assert set({hn.name for hn in host.hostnames}) == {"test.com", "test2.org"}


def test_create_duplicated_hosts(session, workspace):
    assert Host.query.filter(Host.workspace == workspace).count() == 0
    bulk_create(workspace, dict(hosts=[host_data, host_data]))
    db.session.commit()
    assert Host.query.filter(Host.workspace == workspace).count() == 1


def test_create_existing_host(session, host):
    session.add(host)
    session.commit()
    assert Host.query.filter(Host.workspace == host.workspace).count() == 1
    data = {
        "ip": host.ip,
        "description": host.description,
        "hostnames": [hn.name for hn in host.hostnames]
    }
    bulk_create(host.workspace, dict(hosts=[data]))
    assert Host.query.filter(Host.workspace == host.workspace).count() == 1
