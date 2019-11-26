enum class StatusLabel {
    INITIALIZING,
    WAITING_FOR_INPUT,
    BUSY,
};

struct EnhancedStatus : ::enhanced_enum::enum_base<EnhancedStatus, StatusLabel, std::string_view> {
    using ::enhanced_enum::enum_base<EnhancedStatus, StatusLabel, std::string_view>::enum_base;
    static constexpr value_type INITIALIZING_VALUE { "initializing" };
    static constexpr value_type WAITING_FOR_INPUT_VALUE { "waitingForInput" };
    static constexpr value_type BUSY_VALUE { "busy" };
    static constexpr std::array<value_type, 3> values {
        INITIALIZING_VALUE,
        WAITING_FOR_INPUT_VALUE,
        BUSY_VALUE,
    };
};

constexpr EnhancedStatus enhance(StatusLabel e) noexcept
{
    return e;
}

namespace Statuses {
constexpr EnhancedStatus INITIALIZING { StatusLabel::INITIALIZING };
constexpr EnhancedStatus WAITING_FOR_INPUT { StatusLabel::WAITING_FOR_INPUT };
constexpr EnhancedStatus BUSY { StatusLabel::BUSY };
}
