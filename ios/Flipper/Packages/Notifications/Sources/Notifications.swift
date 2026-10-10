import UIKit

/// qAngularity has no push backend (the upstream app used Flipper Devices'
/// Firebase project). The public API is kept so the UI keeps compiling;
/// enabling push simply reports that it is not available.
@MainActor
public class Notifications: NSObject, ObservableObject {
    public static let shared: Notifications = .init()

    public enum Error: Swift.Error {
        case notAllowed
    }

    public var isEnabled: Bool {
        get async { false }
    }

    private override init() {
        super.init()
    }

    public func enable() async throws {
        throw Error.notAllowed
    }

    public func disable() async {
        UIApplication.shared.unregisterForRemoteNotifications()
    }
}
