enum class StatusLabel {
    INITIALIZING,
    WAITING_FOR_INPUT,
    BUSY,
};

struct EnhancedStatus : ::enhanced_enum::enum_base<EnhancedStatus, StatusLabel, std::string_view> {
    using ::enhanced_enum::enum_base<EnhancedStatus, StatusLabel, std::string_view>::enum_base;
    static constexpr std::array values {
        value_type { "initializing" },
        value_type { "waitingForInput" },
        value_type { "busy" },
    };
};

constexpr EnhancedStatus enhance(StatusLabel e) noexcept
{
    return e;
}

namespace Statuses {
inline constexpr const EnhancedStatus::value_type& INITIALIZING_VALUE { std::get<0>(EnhancedStatus::values) };
inline constexpr const EnhancedStatus::value_type& WAITING_FOR_INPUT_VALUE { std::get<1>(EnhancedStatus::values) };
inline constexpr const EnhancedStatus::value_type& BUSY_VALUE { std::get<2>(EnhancedStatus::values) };
inline constexpr EnhancedStatus INITIALIZING { StatusLabel::INITIALIZING };
inline constexpr EnhancedStatus WAITING_FOR_INPUT { StatusLabel::WAITING_FOR_INPUT };
inline constexpr EnhancedStatus BUSY { StatusLabel::BUSY };
inline constexpr auto begin() noexcept { return EnhancedStatus::begin();  }
inline constexpr auto end() noexcept { return EnhancedStatus::end();  }
inline constexpr auto all() noexcept { return EnhancedStatus::all();  }
}
