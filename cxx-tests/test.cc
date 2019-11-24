#include <array>
#include <ostream>

#include <gtest/gtest.h>

#include "status.hh"

using testapp::StatusLabel;
using testapp::EnhancedStatus;
namespace StatusDetails = testapp::StatusDetails;

// Explicitly bundling label enum, enhanced enum and value to be consumed in the
// tests. Also defining operator<< to make the test reports pretty.

struct EnumBundle {
    StatusLabel label;
    EnhancedStatus enhanced;
    std::string_view value;
};

std::ostream& operator<<(std::ostream& os, const EnumBundle& bundle)
{
    return os << bundle.value;
}

// Compiling the test executable is already a test:

static_assert( std::is_trivial_v<EnhancedStatus> );
static_assert( std::is_standard_layout_v<EnhancedStatus> );
static_assert( std::is_same_v<EnhancedStatus::label_type, StatusLabel> );
static_assert( std::is_same_v<EnhancedStatus::value_type, std::string_view> );
static_assert( std::is_same_v<enhanced_enum::enhanced<StatusLabel>, EnhancedStatus> );
static_assert( enhanced_enum::is_enhanced_enum_v<EnhancedStatus> );
static_assert( !enhanced_enum::is_enhanced_enum_v<StatusLabel> );
static_assert( !enhanced_enum::is_label_enum_v<EnhancedStatus> );
static_assert( enhanced_enum::is_label_enum_v<StatusLabel> );
static_assert( std::is_same_v<enhanced_enum::make_enhanced_t<StatusLabel>, EnhancedStatus> );
static_assert( std::is_same_v<enhanced_enum::make_enhanced_t<EnhancedStatus>, EnhancedStatus> );

// enhance(), .get() and .value() are constexpr

static_assert( enhance(StatusLabel::BUSY).get() == StatusLabel::BUSY );
static_assert( enhance(StatusLabel::BUSY).value() == testapp::StatusDetails::BUSY_VALUE );

// Comparison operators work as expected, and can compare both enhanced and
// label enums

static_assert( enhance(StatusLabel::BUSY) == StatusLabel::BUSY );
static_assert( StatusLabel::BUSY == enhance(StatusLabel::BUSY) );

static_assert( enhance(StatusLabel::BUSY) != StatusLabel::INITIALIZING );
static_assert( StatusLabel::BUSY != enhance(StatusLabel::INITIALIZING) );

static_assert( enhance(StatusLabel::INITIALIZING) < StatusLabel::BUSY );
static_assert( StatusLabel::INITIALIZING < enhance(StatusLabel::BUSY) );

static_assert( enhance(StatusLabel::INITIALIZING) <= StatusLabel::BUSY );
static_assert( StatusLabel::INITIALIZING <= enhance(StatusLabel::BUSY) );
static_assert( enhance(StatusLabel::BUSY) <= StatusLabel::BUSY );
static_assert( StatusLabel::BUSY <= enhance(StatusLabel::BUSY) );

static_assert( enhance(StatusLabel::BUSY) > StatusLabel::INITIALIZING );
static_assert( StatusLabel::BUSY > enhance(StatusLabel::INITIALIZING) );

static_assert( enhance(StatusLabel::BUSY) >= StatusLabel::INITIALIZING );
static_assert( StatusLabel::BUSY >= enhance(StatusLabel::INITIALIZING) );
static_assert( enhance(StatusLabel::BUSY) >= StatusLabel::BUSY );
static_assert( StatusLabel::BUSY >= enhance(StatusLabel::BUSY) );

// Non-compile time tests start here:

class EnhancedEnumTest : public testing::TestWithParam<EnumBundle> {};

TEST_P(EnhancedEnumTest, testGetLabelEnum)
{
    const auto bundle = GetParam();
    EXPECT_EQ(bundle.enhanced.get(), bundle.label);
}

TEST_P(EnhancedEnumTest, testValue)
{
    const auto bundle = GetParam();
    EXPECT_EQ(bundle.enhanced.value(), bundle.value);
}

INSTANTIATE_TEST_SUITE_P(
    WithEnumBundle,
    EnhancedEnumTest,
    testing::Values(
        EnumBundle {
            StatusLabel::INITIALIZING,
            enhance(StatusLabel::INITIALIZING),
            StatusDetails::INITIALIZING_VALUE,
        },
        EnumBundle {
            StatusLabel::WAITING_FOR_INPUT,
            enhance(StatusLabel::WAITING_FOR_INPUT),
            StatusDetails::WAITING_FOR_INPUT_VALUE,
        },
        EnumBundle {
            StatusLabel::BUSY,
            enhance(StatusLabel::BUSY),
            StatusDetails::BUSY_VALUE,
        }
    )
);
