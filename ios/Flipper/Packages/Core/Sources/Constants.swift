import Macro
import Foundation

extension String {
    static var appGroup: String {
        "group.com.angularity.qangularity"
    }
}

extension URL {
    static var shareBaseURL = #URL(
        "https://flpr.app/s"
    )
    static var shareFileBaseURL = #URL(
        "https://flpr.app/sf"
    )
    static var transferBaseURL = #URL(
        "https://transfer.flpr.app"
    )
}

extension URL {
    static var firmwareManifestURL = #URL(
        "https://raw.githubusercontent.com/jgm240/angularity-fw/main/ota/directory.json"
    )
}
