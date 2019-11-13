#include "status.hh"

using namespace testapp;

static_assert( std::is_trivial_v<EnhancedStatus> );
static_assert( std::is_standard_layout_v<EnhancedStatus> );
static_assert( std::is_same_v<EnhancedStatus::enum_type, Status> );
static_assert( std::is_same_v<EnhancedStatus::value_type, std::string_view> );
static_assert( enhance(Status::BUSY).get() == Status::BUSY );
static_assert( enhance(Status::INITIALIZING).value() == StatusProperties::INITIALIZING_VALUE );

int main()
{
    return 0;
}
