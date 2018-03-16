import avahi
import dbus
from time import sleep


class ServiceAnnouncer:
    def __init__(self, name, service, port, txt):
        bus = dbus.SystemBus()
        server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), avahi.DBUS_INTERFACE_SERVER)
        group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()),
                               avahi.DBUS_INTERFACE_ENTRY_GROUP)

        self._service_name = name
        index = 1
        while True:
            try:
                group.AddService(avahi.IF_UNSPEC, avahi.PROTO_INET, 0, self._service_name, service, '', '', port, avahi.string_array_to_txt_array(txt))
            except dbus.DBusException: # name collision -> rename
                index += 1
                self._service_name = '%s #%s' % (name, str(index))
            else:
                break

        group.Commit()

    def get_service_name(self):
        return self._service_name


if __name__ == '__main__':
    announcer = ServiceAnnouncer('Test Service', '_test._tcp', 12345, ['foo=bar', '42=true'])
    print announcer.get_service_name()

    sleep(42)
