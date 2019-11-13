#include <enhanced_enum/enhanced_enum.hh>

#include <string_view>

namespace testapp {

enum class Status {
    INITIALIZING,
    WAITING_FOR_INPUT,
    BUSY
};

namespace StatusProperties {
constexpr auto INITIALIZING_VALUE = std::string_view {"initializing"};
constexpr auto WAITING_FOR_INPUT_VALUE = std::string_view {"waitingForInput"};
constexpr auto BUSY_VALUE = std::string_view {"busy"};
};

struct EnhancedStatus : enhanced_enum::enum_base<EnhancedStatus, Status, std::string_view> {
    using enhanced_enum::enum_base<EnhancedStatus, Status, std::string_view>::enum_base;
    static constexpr auto values = std::array {
        StatusProperties::INITIALIZING_VALUE,
        StatusProperties::WAITING_FOR_INPUT_VALUE,
        StatusProperties::BUSY_VALUE,
    };
};

constexpr EnhancedStatus enhance(Status status)
{
    return status;
}

}
